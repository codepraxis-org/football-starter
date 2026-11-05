"""Round 1, mode 1 - Finisher: one attacker with the ball against the goalkeeper.

Tests: shooting angle and timing. Pass: score in enough attempts (see run_round1.py).
Try it: codepraxis-football watch agent.py round1/finisher.py
"""

from codepraxis_football import Level

LEVEL = Level(
    name='r1_finisher',
    description='Beat the goalkeeper.',
    ball=(0.52, 0.0),
    our_players=[(0.5, 0.0, 'CF')],      # (x, y, role); our keeper is added for you
    their_players=[(1.0, 0.0, 'GK')],
    opponent_difficulty=0.6,             # 0 = passive, 1 = strongest built-in AI
    time_limit=400,                      # steps; 10 steps = 1 second
    # The attempt ends on a goal, the ball going out, or losing the ball.
    end_on_goal=True, end_on_ball_out=True, end_on_lost_possession=True,
)
