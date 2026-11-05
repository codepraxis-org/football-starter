"""Round 1: Skills. Runs your agent through 5 short drills and says whether you passed.

    python run_round1.py                # agent.py, all 5 modes (about a minute)
    python run_round1.py my_agent.py    # another agent file
    python run_round1.py --only 2       # just mode 2
    python run_round1.py --quick        # a quarter of the episodes

Watch a mode: codepraxis-football watch agent.py round1/dribbler.py
"""

import sys

from runner import Mode, run_round

# Targets sit just above the best our own agents reached (starter agent.py, the built-in AI,
# a tuned rule-based agent): Finisher 50%, Dribbler 9%, Chased 36%, Playmaker 21%, Counter 15%.
MODES = [
    Mode('Finisher', 'round1/finisher.py', 100, 'goal_rate', 0.55, chunk=25),
    Mode('Dribbler', 'round1/dribbler.py', 100, 'goal_rate', 0.12, chunk=25),
    Mode('Chased', 'round1/chased.py', 100, 'goal_rate', 0.40, chunk=25),
    Mode('Playmaker', 'round1/playmaker.py', 100, 'goal_rate', 0.25, chunk=25),
    Mode('Counter', 'round1/counter.py', 100, 'goal_rate', 0.20, chunk=25),
]
MUST_PASS = 4  # of 5

if __name__ == '__main__':
  sys.exit(0 if run_round('Round 1 (Skills)', MODES, MUST_PASS) else 1)
