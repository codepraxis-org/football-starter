"""Round 1, mode 4 - Playmaker: 3 attackers against 1 defender and the goalkeeper.

Tests: passing. You control whichever attacker is nearest the ball, so a pass hands
control to the receiver.
Try it: codepraxis-football watch agent.py round1/playmaker.py
"""

from codepraxis_football import Level

LEVEL = Level(
    name='r1_playmaker',
    description='3 vs 1 and the keeper: pass and score.',
    ball=(0.62, 0.0),
    our_players=[(0.6, 0.0, 'CM'), (0.7, 0.2, 'CM'), (0.7, -0.2, 'CM')],
    their_players=[(1.0, 0.0, 'GK'), (0.75, 0.0, 'CB')],
    opponent_difficulty=0.6,
    time_limit=400,
    end_on_goal=True, end_on_ball_out=True, end_on_lost_possession=True,
)
