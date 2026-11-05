# CodePraxis Football

Write a Python agent that plays football. Pass Round 1 (skills) and Round 2 (matches), then meet
another agent in the Final. Everything runs on your laptop.

## Setup (5 minutes)

Python 3.12+ and git; macOS, Linux or Windows; no GPU.

```sh
git clone https://github.com/codepraxis-org/football-starter.git
cd football-starter
python3 -m venv .venv
source .venv/bin/activate                 # Windows: .venv\Scripts\activate
pip install "codepraxis-football>=0.3.0"
codepraxis-football doctor                # every line should say [ok]
codepraxis-football watch agent.py match_5v5.py   # the sample agent plays 5 vs 5
```

Run everything from inside `football-starter`. Linux server: `sudo apt install libgl1 libegl1` first.

## How an agent works

`agent.py` is the only file you change. One agent plays every mode in every round.

```python
from codepraxis_football import Action

def agent(obs):                      # called 10 times per second of game time
    me = obs['left_team'][obs['active']]  # the player you control: nearest to the ball
    if me[0] > 0.7:                   # x: -1 our goal .. 1 their goal
        return Action.SHOT
    return Action.RIGHT               # one action per step
```

- `obs` is what your player sees: ball, every player's position and direction, score, game mode.
- You return one of 19 actions: 8 directions, passes, shot, sprint, dribble, tackle.
- The sample `agent.py` chases the ball, passes when blocked and shoots near goal. Start from it.
- Name your team and pick colours at the top: `TEAM_NAME`, `SHIRT_COLOR`, `SHORTS_COLOR`.

Every field and action: [docs/agent-reference.md](docs/agent-reference.md).

## Round 1: Skills

Short drills. Each attempt ends on a goal, the ball going out, or losing it.

| # | Mode | You have to | Pass |
|---|---|---|---|
| 1 | Finisher | beat the goalkeeper, 1 vs 1 | score in 55% |
| 2 | Dribbler | get past 3 defenders and the keeper | score in 12% |
| 3 | Chased | outrun 5 defenders chasing from behind | score in 40% |
| 4 | Playmaker | 3 vs 1 + keeper: pass and score | score in 25% |
| 5 | Counter | finish a 4 vs 1 counter-attack | score in 20% |

**Round passed: 4 of 5 modes.**

Test one mode by watching it:
```sh
codepraxis-football watch agent.py round1/dribbler.py
```

Test the whole round (headless, all CPU cores, about 15 seconds):
```sh
python run_round1.py               # 100 attempts per mode, PASS/FAIL per mode, verdict
python run_round1.py --only 2      # one mode
```

## Round 2: Matches

| # | Mode | You have to | Pass |
|---|---|---|---|
| 1 | 5v5 | beat the built-in AI (difficulty 0.5) | win 85% of 8 matches |
| 2 | 5v5 Pro | beat the strongest built-in AI (1.0) | win 25% of 8 matches |
| 3 | Defender | stop a 4 vs 2 attack on your goal | concede in at most 3% of 100 |
| 4 | 11v11 | full match against the built-in AI (0.5) | win by 2+ goals a match, 6 matches |

**Round passed: 3 of 4 modes.** The marks are set above the game's own AI: copying what the
built-in players do is not enough.

Test one mode by watching it:
```sh
codepraxis-football watch agent.py round2/match_5v5.py      # a 5-minute match, real time
```

Test the whole round (headless, about 30 seconds):
```sh
python run_round2.py
python run_round2.py --only 3
```

## Final: agent against agent

11 vs 11. Each agent controls its player nearest the ball; the built-in AI plays everyone else,
equally strong on both sides. Sides swap every match. Winner: more matches won, then goal difference.

Watch a match:
```sh
python run_final.py agent.py other_agent.py --watch     # --fps 20 for double speed
```

Play a series headless (about a minute):
```sh
python run_final.py agent.py other_agent.py             # 4 matches; --matches 8 for more
python run_final.py agent.py agent.py                   # no opponent yet? play yourself
```

## Good to know

- These are practice seeds. Judging uses the same modes and marks with seeds you haven't seen.
- Results are exact: the same agent gets the same score every run.
- `--quick` on the round scripts runs a quarter of the attempts: faster, noisier.
- More: [all commands](docs/commands.md) (play it yourself, videos, scoring one mode),
  [game modes](docs/game-modes.md) (their settings, making your own),
  [agent reference](docs/agent-reference.md).
