"""Final: 11 vs 11, agent against agent. Each agent controls its player nearest the ball;
the built-in AI plays everyone else, equally strong on both sides.

Try it: python run_final.py agent.py other_agent.py --watch
"""

from codepraxis_football import Level

# A 4-3-3 for both sides; keepers are added for you.
_OUTFIELD = [(-0.422, -0.196, 'LB'), (-0.5, -0.064, 'CB'), (-0.5, 0.064, 'CB'), (-0.422, 0.196, 'RB'),
             (-0.184, -0.106, 'CM'), (-0.268, 0.0, 'CM'), (-0.184, 0.106, 'CM'),
             (-0.01, -0.216, 'LM'), (0.0, -0.02, 'CF'), (0.0, 0.02, 'RM')]

LEVEL = Level(
    name='final_match_11v11',
    description='11 vs 11, agent against agent.',
    ball=(0.0, 0.0),
    our_players=_OUTFIELD,
    their_players=[(1.0, 0.0, 'GK')] + [(-x + (0.05 if r in ('CF', 'RM') else 0), -y, r)
                                        for x, y, r in _OUTFIELD],
    opponent_difficulty=0.6,   # the built-in AI helping each side: same strength for both
    teammate_difficulty=0.6,
    time_limit=3000,           # 5 minutes of game time
    end_on_goal=False, end_on_ball_out=False, end_on_lost_possession=False,
)
