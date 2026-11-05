"""Round 2, mode 1 - 5 vs 5 match against the built-in AI at difficulty 0.5.

Tests: everything at once: attacking, passing, defending, set pieces. Pass: win the matches.
Try it: codepraxis-football watch agent.py round2/match_5v5.py
"""

from codepraxis_football import Level

LEVEL = Level(
    name='r2_match_5v5',
    description='5 vs 5 match, opponent difficulty 0.5.',
    ball=(0.0, 0.0),
    our_players=[(-0.02, 0.0, 'CF'), (-0.02, 0.1, 'RM'), (-0.25, -0.1, 'LB'), (-0.25, 0.1, 'CB')],
    their_players=[(1.0, 0.0, 'GK'), (0.04, 0.04, 'RM'), (0.04, -0.04, 'CF'),
                   (0.25, -0.1, 'LB'), (0.25, 0.1, 'CB')],
    opponent_difficulty=0.5,   # 0 = stands still, 1 = strongest built-in AI
    time_limit=3000,           # 5 minutes of game time
    # A match plays on after goals, throw-ins and lost balls.
    end_on_goal=False, end_on_ball_out=False, end_on_lost_possession=False,
)
