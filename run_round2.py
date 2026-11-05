"""Round 2: Matches. Runs your agent through 4 match modes and says whether you passed.

    python run_round2.py                # agent.py, all 4 modes (a few minutes)
    python run_round2.py my_agent.py    # another agent file
    python run_round2.py --only 1       # just mode 1
    python run_round2.py --quick        # a quarter of the matches

Watch a mode: codepraxis-football watch agent.py round2/match_5v5.py
"""

import sys

from runner import Mode, run_round

# Targets sit above the built-in AI playing your player (5v5: 6 of 8 won, Pro: 1 of 8,
# Defender: conceded 5%, 11v11: +1.5 goals a match), so matching the game's own AI is not enough.
MODES = [
    Mode('5v5', 'round2/match_5v5.py', 8, 'win_rate', 0.85, chunk=1),
    Mode('5v5 Pro', 'round2/match_5v5_pro.py', 8, 'win_rate', 0.25, chunk=1),
    Mode('Defender', 'round2/defender.py', 100, 'concede_rate', 0.03, chunk=20),
    Mode('11v11', 'round2/match_11v11.py', 6, 'goal_diff', 2.0, chunk=1),
]
MUST_PASS = 3  # of 4

if __name__ == '__main__':
  sys.exit(0 if run_round('Round 2 (Matches)', MODES, MUST_PASS) else 1)
