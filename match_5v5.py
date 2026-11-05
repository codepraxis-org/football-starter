"""The game mode: a 5 vs 5 match. Every setting of the game lives here.

Use this file anywhere a level name goes:
    codepraxis-football watch agent.py match_5v5.py
    codepraxis-football eval agent.py match_5v5.py --episodes 20

Copy it to make your own mode (harder opponent, longer match, different line-up).
Pitch: x from -1 (our goal) to 1 (their goal), y from -0.42 (top) to 0.42 (bottom).
"""

from codepraxis_football import Level

LEVEL = Level(
    name='match_5v5',
    description='5 vs 5 match against the built-in AI.',

    # Who plays where: (x, y, role). Roles: GK, CB, LB, RB, DM, CM, LM, RM, AM, CF.
    # Our goalkeeper is added at (-1, 0) when the list has no GK.
    ball=(0.0, 0.0),
    our_players=[(-0.02, 0.0, 'CF'), (-0.02, 0.1, 'RM'), (-0.25, -0.1, 'LB'), (-0.25, 0.1, 'CB')],
    their_players=[(1.0, 0.0, 'GK'), (0.04, 0.04, 'RM'), (0.04, -0.04, 'CF'),
                   (0.25, -0.1, 'LB'), (0.25, 0.1, 'CB')],

    # How strong the other team is: 0 = stands still, 1 = strongest built-in AI.
    opponent_difficulty=0.6,

    # Match length in steps; 10 steps = 1 second of game time. 3000 = 5 minutes.
    time_limit=3000,

    # A match plays on after goals, throw-ins and lost balls (drills end on them).
    end_on_goal=False,
    end_on_ball_out=False,
    end_on_lost_possession=False,
    offsides=False,
)
