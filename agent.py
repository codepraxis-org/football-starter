"""A rule-based agent for the 5 vs 5 match. Edit me.

Run it:
    codepraxis-football watch agent.py match_5v5.py               # watch it play, live window
    codepraxis-football eval agent.py match_5v5.py --episodes 10  # score it (JSON)

You control one player at a time: the one nearest the ball. Your other players and the
opponents are played by the built-in AI.

Pitch: x from -1 (our goal) to 1 (the goal we attack), y from -0.42 (top) to 0.42 (bottom).
"""

import math

from codepraxis_football import Action

OBSERVATION = 'raw'  # obs is a dict; README.md lists every field
PLAYERS = 1          # how many of our players this agent controls

# The knobs worth tuning first.
SHOOT_FROM_X = 0.72    # shoot once this close to their goal...
SHOOT_MAX_Y = 0.22     # ...and this central
PRESSURE = 0.09        # an opponent this close in front: pass instead of dribbling
LOOK_AHEAD = 4         # steps: run to where the ball will be, not where it is

GOAL = (1.0, 0.0)
NORMAL, KICK_OFF, GOAL_KICK, FREE_KICK, CORNER, THROW_IN, PENALTY = range(7)

# 8 moves, counter-clockwise from "right", 45 degrees apart
COMPASS = [Action.RIGHT, Action.TOP_RIGHT, Action.TOP, Action.TOP_LEFT,
           Action.LEFT, Action.BOTTOM_LEFT, Action.BOTTOM, Action.BOTTOM_RIGHT]


def move_towards(me, target):
  dx, dy = target[0] - me[0], target[1] - me[1]
  angle = math.atan2(-dy, dx)  # y grows downwards, so flip it
  return COMPASS[round(angle / (math.pi / 4)) % 8]


def distance(a, b):
  return math.hypot(a[0] - b[0], a[1] - b[1])


class Agent:

  def reset(self):  # start of every match
    self.facing = None  # direction set up for a pass or shot, used on the next step

  def act(self, obs):
    me = obs['left_team'][obs['active']]
    ball = obs['ball'][:2]
    they = obs['right_team']
    i_have_ball = obs['ball_owned_team'] == 0 and obs['ball_owned_player'] == obs['active']

    # Set pieces (kick-off, free kick, corner, throw-in...): play it short and get going.
    if obs['game_mode'] != NORMAL and i_have_ball:
      return Action.SHORT_PASS

    # Passes and shots go the way the player faces: face first, kick on the next step.
    if self.facing is not None:
      kick, self.facing = self.facing, None
      if i_have_ball:
        return kick

    sprinting = obs['sticky_actions'][8]  # 8 directions first, then sprint, then dribble
    if not sprinting:
      return Action.SPRINT

    if not i_have_ball:
      # Chase the ball: aim where it is going.
      dx, dy = obs['ball_direction'][:2]
      return move_towards(me, (ball[0] + LOOK_AHEAD * dx, ball[1] + LOOK_AHEAD * dy))

    if me[0] > SHOOT_FROM_X and abs(me[1]) < SHOOT_MAX_Y:
      self.facing = Action.SHOT
      return move_towards(me, GOAL)

    # An opponent right in front: pass to the teammate furthest up the pitch.
    blocked = any(0 < o[0] - me[0] < PRESSURE and abs(o[1] - me[1]) < PRESSURE for o in they)
    if blocked:
      mates = [p for i, p in enumerate(obs['left_team']) if i not in (0, obs['active'])]
      best = max(mates, key=lambda p: p[0])
      if best[0] > me[0] - 0.05:
        self.facing = Action.SHORT_PASS
        return move_towards(me, best)

    # Otherwise run at goal, drifting away from the nearest opponent.
    nearest = min(they, key=lambda o: distance(o, me))
    swerve = 0.15 if nearest[1] < me[1] else -0.15
    return move_towards(me, (GOAL[0], GOAL[1] + (swerve if distance(nearest, me) < 0.2 else 0)))
