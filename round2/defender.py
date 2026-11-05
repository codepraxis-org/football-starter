"""Round 2, mode 3 - Defender: they attack your goal, 4 against your 2 defenders and keeper.

Tests: defending. Your teammates get little help from the built-in AI here, so it is up to
the player you control. The attempt ends when you win the ball, it goes out, they score,
or 30 seconds pass. Pass: concede in few enough attempts (see run_round2.py).
Try it: codepraxis-football watch agent.py round2/defender.py
"""

from codepraxis_football import Level

LEVEL = Level(
    name='r2_defender',
    description='Stop a 4 vs 2 attack on your goal.',
    ball=(-0.4, 0.0),
    our_players=[(-0.72, -0.1, 'CB'), (-0.72, 0.1, 'CB')],
    their_players=[(1.0, 0.0, 'GK'), (-0.42, 0.0, 'CF'), (-0.35, -0.2, 'LM'), (-0.35, 0.2, 'RM'),
                   (-0.25, 0.0, 'AM')],
    opponent_difficulty=0.9,
    teammate_difficulty=0.3,   # the built-in AI barely helps your other defenders
    time_limit=300,            # 30 seconds
    end_on_goal=True, end_on_ball_out=True, end_on_lost_possession=True,
)
