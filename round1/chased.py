"""Round 1, mode 3 - Chased: from the halfway line, 5 defenders chasing from behind.

Tests: speed, a straight line to goal, finishing under pressure.
Try it: codepraxis-football watch agent.py round1/chased.py
"""

from codepraxis_football import Level

LEVEL = Level(
    name='r1_chased',
    description='Outrun 5 chasing defenders and beat the keeper.',
    ball=(0.02, 0.0),
    our_players=[(0.0, 0.0, 'CF')],
    their_players=[(1.0, 0.0, 'GK'), (-0.12, -0.2, 'LB'), (-0.12, -0.1, 'CB'), (-0.12, 0.0, 'CM'),
                   (-0.12, 0.1, 'CB'), (-0.12, 0.2, 'RB')],
    opponent_difficulty=0.6,
    time_limit=400,
    end_on_goal=True, end_on_ball_out=True, end_on_lost_possession=True,
)
