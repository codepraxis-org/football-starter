"""Round 2, mode 4 - Full match: 11 vs 11 against the built-in AI at difficulty 0.5.

Tests: a bigger pitch and more players to read. You control whichever player is nearest the ball.
Try it: codepraxis-football watch agent.py round2/match_11v11.py
"""

from codepraxis_football import Level

# A 4-3-3 for both sides; our keeper is added for you.
_OUTFIELD = [(-0.422, -0.196, 'LB'), (-0.5, -0.064, 'CB'), (-0.5, 0.064, 'CB'), (-0.422, 0.196, 'RB'),
             (-0.184, -0.106, 'CM'), (-0.268, 0.0, 'CM'), (-0.184, 0.106, 'CM'),
             (-0.01, -0.216, 'LM'), (0.0, -0.02, 'CF'), (0.0, 0.02, 'RM')]

LEVEL = Level(
    name='r2_match_11v11',
    description='11 vs 11 match, opponent difficulty 0.5.',
    ball=(0.0, 0.0),
    our_players=_OUTFIELD,
    their_players=[(1.0, 0.0, 'GK')] + [(-x + (0.05 if r in ('CF', 'RM') else 0), -y, r)
                                        for x, y, r in _OUTFIELD],
    opponent_difficulty=0.5,
    time_limit=3000,
    end_on_goal=False, end_on_ball_out=False, end_on_lost_possession=False,
)
