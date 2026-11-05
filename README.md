# CodePraxis Football: 5 vs 5 starter

Write a Python agent that plays football, watch it play, and score it, all on your laptop.

| File | What it is |
|---|---|
| `agent.py` | The agent: a rule-based 5 vs 5 player. Edit this. |
| `match_5v5.py` | The game mode: line-up, opponent strength, match length. Copy it to make your own. |

## Install

Python 3.12 or newer; macOS, Linux or Windows. No GPU needed.

```sh
pip install codepraxis-football
codepraxis-football doctor          # checks the engine, rendering and video
```

On a Linux server or minimal Linux install: `sudo apt install libgl1 libegl1`.

## Play, watch, score

One command: what to do, the agent, the game mode.

```sh
codepraxis-football play match_5v5.py                          # you play, with the keyboard
codepraxis-football watch agent.py match_5v5.py                # watch the agent, live window
codepraxis-football eval agent.py match_5v5.py --episodes 10   # score it: wins, goals (JSON)
codepraxis-football video agent.py match_5v5.py --view topdown -o match.mp4
codepraxis-football watch-match agent.py random match_5v5.py   # two agents, yellow vs blue
codepraxis-football match agent.py other_agent.py match_5v5.py # head to head, no window
```

A 5-minute match (3,000 steps) takes about 5 seconds in `eval`. `watch` plays it in real time.
`random` and `idle` work in place of an agent file; `builtin` (the game's own AI playing your
player) works in `watch` and `eval`, not in head-to-head `match` / `watch-match`.

Keyboard in `play` (click the window first): arrows move, hold `e` sprint, hold `c` dribble,
`s` short pass, `a` high pass, `w` long pass, `d` shoot, `x` slide tackle, `Esc` quit.

## Make it better

The loop: change `agent.py`, `watch` to see what it does, `eval` to measure it.

Start with the knobs at the top of `agent.py`:

| Knob | Default | Effect |
|---|---|---|
| `SHOOT_FROM_X` | 0.72 | How close to goal before shooting |
| `SHOOT_MAX_Y` | 0.22 | How central a shot must be |
| `PRESSURE` | 0.09 | How close a defender gets before we pass |
| `LOOK_AHEAD` | 4 | How far ahead of the ball we run, in steps |

Then the rules themselves: when to pass and to whom, through balls (`LONG_PASS`), dribbling
(`DRIBBLE`), defending (positioning, `SLIDING`), set pieces. Ideas for later: control more players
(`PLAYERS = 4`), or train a model instead of writing rules (see "Reinforcement learning" in
`codepraxis-football init`'s guide).

What this agent scores, 10 matches against difficulty 0.6:

| Our player controlled by | Won / drawn / lost | Goals |
|---|---|---|
| `agent.py` | 8 / 2 / 0 | 20-2 |
| `builtin` | 1 / 9 / 0 | 3-2 |
| `idle` | 0 / 10 / 0 | 0-0 |

Raise `opponent_difficulty` in `match_5v5.py` to 1.0 for a real fight.

## Game mode settings (`match_5v5.py`)

| Setting | Meaning |
|---|---|
| `our_players`, `their_players` | `(x, y, role)` per player. Our goalkeeper is added unless listed |
| `ball` | Where the ball starts |
| `opponent_difficulty` | 0 (stands still) to 1 (strongest built-in AI) |
| `time_limit` | Steps; 10 steps = 1 second of game time |
| `end_on_goal`, `end_on_ball_out`, `end_on_lost_possession` | End the episode then (drills) or play on (matches) |
| `offsides` | Offside rule on or off |

Built-in modes work by name too: `codepraxis-football levels` lists them (drills like `shoot_keeper`,
full `match_11v11`).

## Writing an agent

An agent is a file with a function `agent(obs)` or a class `Agent` with `act(obs)` (and an optional
`reset()` at the start of each match). It returns one action per step, 10 steps per second of game time.
A step slower than 50 ms counts as doing nothing.

Settings at the top of the file:

| Setting | Default | Meaning |
|---|---|---|
| `OBSERVATION` | `'raw'` | `'raw'` (dict below), `'vector'` (115 numbers), `'minimap'`, `'pixels'` |
| `PLAYERS` | `1` | How many of our players you control. More than 1: `obs` is a list, return a list |

### The pitch

`x` runs from -1 (our goal) to 1 (the goal you attack); `y` from -0.42 (top) to 0.42 (bottom).
You always attack to the right, also when your agent plays the other side in `match`.

### What the agent sees (`OBSERVATION = 'raw'`)

| Field | Meaning |
|---|---|
| `ball` | `[x, y, z]` ball position (z = height) |
| `ball_direction` | `[x, y, z]` ball movement per step |
| `ball_owned_team` | -1 nobody, 0 us, 1 them |
| `ball_owned_player` | index of the player with the ball |
| `left_team`, `right_team` | `[x, y]` of every player (left = us; index 0 is the keeper) |
| `left_team_direction`, `right_team_direction` | movement per step of every player |
| `left_team_roles`, `right_team_roles` | 0 GK, 1 CB, 2 LB, 3 RB, 4 DM, 5 CM, 6 LM, 7 RM, 8 AM, 9 CF |
| `left_team_tired_factor`, `right_team_tired_factor` | 0 fresh to 1 exhausted |
| `left_team_yellow_card`, `left_team_active` (and right) | cards; `active` False = sent off |
| `active` | index (in `left_team`) of the player you control |
| `sticky_actions` | 10 flags: 8 directions, sprint, dribble (on until released) |
| `score` | `[ours, theirs]` |
| `steps_left` | steps until the match ends |
| `game_mode` | 0 normal, 1 kick-off, 2 goal kick, 3 free kick, 4 corner, 5 throw-in, 6 penalty |

### Actions

| # | Action | # | Action |
|---|---|---|---|
| 0 | IDLE | 10 | HIGH_PASS |
| 1-8 | LEFT, TOP_LEFT, TOP, TOP_RIGHT, RIGHT, BOTTOM_RIGHT, BOTTOM, BOTTOM_LEFT | 11 | SHORT_PASS |
| 9 | LONG_PASS | 12 | SHOT |
| 13 | SPRINT | 14 | RELEASE_DIRECTION |
| 15 | RELEASE_SPRINT | 16 | SLIDING |
| 17 | DRIBBLE | 18 | RELEASE_DRIBBLE |

Directions, sprint and dribble stay on until released. Passes and shots go the way the player faces.

## Good to know

- `eval` and top-down videos are exact: same seed, same match. The 3D window and 3D videos run extra
  engine code, so a match there can play out differently from the scored one.
- Full guide (training with Python, reinforcement learning, practice levels):
  `codepraxis-football init guide` writes it to `guide/README.md`.
