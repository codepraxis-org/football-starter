"""Round 1, mode 2 - Dribbler: get past 3 defenders and the goalkeeper.

Tests: dribbling, changing direction, avoiding tackles.
Try it: codepraxis-football watch agent.py round1/dribbler.py
"""

from codepraxis_football import Level

LEVEL = Level(
    name='r1_dribbler',
    description='Get past 3 defenders and score.',
    ball=(0.27, 0.0),
    our_players=[(0.25, 0.0, 'CF')],
    their_players=[(1.0, 0.0, 'GK'), (0.55, -0.1, 'CB'), (0.5, 0.0, 'CB'), (0.55, 0.1, 'CB')],
    opponent_difficulty=0.6,
    time_limit=400,
    end_on_goal=True, end_on_ball_out=True, end_on_lost_possession=True,
)
