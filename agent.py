"""The sample agent: a simple football player written as a list of rules. Edit me.

THE BIG PICTURE
---------------
The game asks your agent for a decision 10 times per second of game time. Each time it hands
over `obs` (what your player sees: where the ball and every player are) and you hand back ONE
action (run in a direction, pass, shoot, sprint...).

You control one player at a time: the one of your team nearest the ball. The game's own AI
plays everyone else (your teammates and the opponents). When the ball moves to another of
your players, control moves with it.

HOW THIS AGENT DECIDES
----------------------
`act()` below goes through these rules from top to bottom and does the FIRST one that applies:

  1. Set piece (kick-off, free kick, corner, throw-in) and we have the ball -> short pass.
  2. Last step we turned to aim a pass or shot -> now kick it.
  3. Not sprinting yet -> switch sprint on (it stays on).
  4. We don't have the ball -> run to where the ball is going.
  5. Close to their goal and central -> turn to the goal (rule 2 shoots next step).
  6. An opponent right in front and a teammate further forward -> turn to him (rule 2 passes).
  7. Otherwise -> run at their goal, swerving away from the nearest opponent.

That's all. It is deliberately simple: it never defends on purpose, never dribbles, never uses
long passes and doesn't think about teammates' space. Those are your improvements to make.

THE PITCH (the same for every mode and both sides: you always attack to the right)
---------
           x = -1                     x = 0                      x = 1
  y = -0.42 +---------------------------+---------------------------+
            |                           |                           |
          [ ]  our goal (-1, 0)         o  centre (0, 0)     their goal (1, 0)  [ ]
            |                           |                           |
  y = 0.42  +---------------------------+---------------------------+

  Positions are (x, y). y grows DOWNWARDS (top of the screen is negative).

TRY IT
------
    codepraxis-football watch agent.py match_5v5.py     # watch it play a match
    python run_round1.py                                # score it on Round 1
Every field of `obs` and every action: docs/agent-reference.md
"""

import math

from codepraxis_football import Action

# --- Settings the game reads -------------------------------------------------------------------

OBSERVATION = 'raw'  # obs is a dict of named fields (the easiest to write rules with)
PLAYERS = 1          # we control 1 player: the one nearest the ball

# Your team's look; no effect on play. Colours: '#rrggbb', a name like 'red', or (r, g, b).
TEAM_NAME = 'CodePraxis FC'
SHIRT_COLOR = '#1e5fbf'
SHORTS_COLOR = 'white'

# --- Knobs: the numbers worth tuning first -------------------------------------------------------

SHOOT_FROM_X = 0.72  # rule 5: shoot only once past this x (their goal is at x = 1)...
SHOOT_MAX_Y = 0.22   # ...and only if this close to the middle (|y| below this)
PRESSURE = 0.09      # rule 6: an opponent this close in front of us means "blocked"
LOOK_AHEAD = 4       # rule 4: run to where the ball will be in this many steps

# --- Fixed facts ------------------------------------------------------------------------------

GOAL = (1.0, 0.0)  # the middle of the goal we attack

# obs['game_mode'] values: 0 is normal play, the rest are set pieces.
NORMAL, KICK_OFF, GOAL_KICK, FREE_KICK, CORNER, THROW_IN, PENALTY = range(7)

# The 8 run directions, going round anticlockwise from "right", 45 degrees apart.
COMPASS = [Action.RIGHT, Action.TOP_RIGHT, Action.TOP, Action.TOP_LEFT,
           Action.LEFT, Action.BOTTOM_LEFT, Action.BOTTOM, Action.BOTTOM_RIGHT]


# --- Helpers ----------------------------------------------------------------------------------

def move_towards(me, target):
  """The one of the 8 run directions that points most closely from `me` to `target`.

  Example: me = (0, 0), target = (1, -1) -> up and to the right -> Action.TOP_RIGHT.
  """
  dx, dy = target[0] - me[0], target[1] - me[1]
  angle = math.atan2(-dy, dx)  # the angle of the arrow; y is flipped because it grows downwards
  return COMPASS[round(angle / (math.pi / 4)) % 8]  # snap to the nearest 45 degrees


def distance(a, b):
  """Straight-line distance between two (x, y) points."""
  return math.hypot(a[0] - b[0], a[1] - b[1])


# --- The agent --------------------------------------------------------------------------------

class Agent:
  """A class (not just a function) because rule 2 must remember what it planned last step."""

  def reset(self):
    """Called at the start of every attempt or match: forget last game's plan."""
    self.facing = None  # a pass or shot we turned towards last step, to kick this step

  def act(self, obs):
    """Called every step. Looks at `obs`, returns one action."""

    # What we look at, in plain names.
    me = obs['left_team'][obs['active']]  # (x, y) of the player we control; left_team = us
    ball = obs['ball'][:2]                # (x, y) of the ball; [2] would be its height
    they = obs['right_team']              # (x, y) of every opponent; index 0 is their keeper
    i_have_ball = obs['ball_owned_team'] == 0 and obs['ball_owned_player'] == obs['active']

    # Rule 1. Set pieces (kick-off, free kick, corner, throw-in...): the game waits for us to
    # play the ball, so play it short to a teammate and get going.
    # Better: pick the receiver, or shoot from a free kick near goal.
    if obs['game_mode'] != NORMAL and i_have_ball:
      return Action.SHORT_PASS

    # Rule 2. Passes and shots go the way the player is FACING, not towards a target. So kicking
    # takes two steps: rules 5 and 6 turn the player and remember the kick in `self.facing`;
    # this rule kicks on the next step (if we still have the ball).
    if self.facing is not None:
      kick, self.facing = self.facing, None
      if i_have_ball:
        return kick

    # Rule 3. Sprint is a switch: SPRINT turns it on and it stays on until RELEASE_SPRINT.
    # sticky_actions holds those switches: [0-7] the 8 directions, [8] sprint, [9] dribble.
    # This agent sprints all the time. Better: sprinting tires players and makes the ball harder
    # to control; release it near goal or when dribbling past someone.
    sprinting = obs['sticky_actions'][8]
    if not sprinting:
      return Action.SPRINT

    # Rule 4. Without the ball: chase it. Not to where it is, but to where it is going:
    # ball_direction is how far it moves per step, so ball + 4 * direction is its spot in 4 steps.
    # Better: if a teammate is closer, take up a useful position instead of everyone chasing.
    if not i_have_ball:
      dx, dy = obs['ball_direction'][:2]
      return move_towards(me, (ball[0] + LOOK_AHEAD * dx, ball[1] + LOOK_AHEAD * dy))

    # From here on we have the ball.

    # Rule 5. Close to goal and central enough to have an angle: turn to the goal; rule 2
    # shoots on the next step.
    # Better: aim for the corner away from the keeper (they[0] is their keeper's position).
    if me[0] > SHOOT_FROM_X and abs(me[1]) < SHOOT_MAX_Y:
      self.facing = Action.SHOT
      return move_towards(me, GOAL)

    # Rule 6. An opponent right in front of us (within PRESSURE ahead and to the side): pass to
    # the teammate furthest up the pitch, if he is not behind us. mates leaves out our keeper
    # (index 0) and ourselves. Some modes have no teammates: then there is no one to pass to.
    # Better: pass to the teammate with the most space, not just the furthest forward.
    blocked = any(0 < o[0] - me[0] < PRESSURE and abs(o[1] - me[1]) < PRESSURE for o in they)
    mates = [p for i, p in enumerate(obs['left_team']) if i not in (0, obs['active'])]
    if blocked and mates:
      best = max(mates, key=lambda p: p[0])  # furthest forward = largest x
      if best[0] > me[0] - 0.05:
        self.facing = Action.SHORT_PASS
        return move_towards(me, best)

    # Rule 7. Nothing else applies: run at their goal. If an opponent (their keeper counts) is
    # within 0.2, aim 0.15 to the side away from him: that dodges him and opens a shooting angle.
    # Better: look further ahead, use DRIBBLE to keep the ball close, or cut inside late.
    nearest = min(they, key=lambda o: distance(o, me))
    swerve = 0.15 if nearest[1] < me[1] else -0.15  # he is above us -> aim lower, and vice versa
    aim_y = GOAL[1] + (swerve if distance(nearest, me) < 0.2 else 0)
    return move_towards(me, (GOAL[0], aim_y))
