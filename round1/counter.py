"""Round 1, mode 5 - Counter: a fast break, 4 attackers against 1 defender, full teams on the pitch.

Tests: reading a moving situation and finishing before defenders get back.
Try it: codepraxis-football watch agent.py round1/counter.py
"""

from codepraxis_football import Level

LEVEL = Level(
    name='r1_counter',
    description='Finish a 4 vs 1 counter-attack.',
    ball=(0.26, -0.11),
    our_players=[(-0.672, -0.196, 'LB'), (-0.75, -0.064, 'CB'), (-0.75, 0.064, 'CB'), (-0.672, 0.196, 'RB'),
                 (-0.434, -0.106, 'CM'), (-0.434, 0.106, 'CM'), (0.5, -0.316, 'CM'),
                 (0.25, -0.1, 'LM'), (0.25, 0.1, 'RM'), (0.35, 0.316, 'CF')],
    their_players=[(1.0, 0.0, 'GK'), (-0.128, 0.196, 'LB'), (-0.4, 0.064, 'CB'), (0.4, -0.064, 'CB'),
                   (-0.128, 0.196, 'RB'), (-0.365, 0.106, 'CM'), (-0.282, 0.0, 'CM'), (-0.365, -0.106, 'CM'),
                   (-0.54, 0.316, 'LM'), (-0.51, 0.0, 'RM'), (-0.54, -0.316, 'CF')],
    opponent_difficulty=0.6,
    time_limit=400,
    end_on_goal=True, end_on_ball_out=True, end_on_lost_possession=True,
)
