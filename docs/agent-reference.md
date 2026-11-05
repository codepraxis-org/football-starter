# Agent reference

An agent is a Python file with a function `agent(obs)`, or a class `Agent` with `act(obs)` and an
optional `reset()` (called at the start of every attempt or match). It returns one action per step.
The game runs 10 steps per second of game time. A step slower than 50 ms counts as IDLE.

## Settings at the top of the file

| Setting | Default | Meaning |
|---|---|---|
| `OBSERVATION` | `'raw'` | `'raw'` (dict below), `'vector'` (115 numbers), `'minimap'`, `'pixels'` |
| `PLAYERS` | `1` | How many of our players you control (the nearest to the ball first). More than 1: `obs` is a list, return a list |
| `TEAM_NAME` | `'CodePraxis FC'` | Shown on the scoreboard; looks only |
| `SHIRT_COLOR`, `SHORTS_COLOR` | blue, white | `'red'`, `'#e53935'` or `(229, 57, 53)`; looks only |

## The pitch

`x` runs from -1 (our goal) to 1 (the goal you attack); `y` from -0.42 (top) to 0.42 (bottom).
You always attack to the right, also when your agent plays the other side in the final.

## What the agent sees (`OBSERVATION = 'raw'`)

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
| `steps_left` | steps until the attempt or match ends |
| `game_mode` | 0 normal, 1 kick-off, 2 goal kick, 3 free kick, 4 corner, 5 throw-in, 6 penalty |

## Actions

| # | Action | # | Action |
|---|---|---|---|
| 0 | IDLE | 10 | HIGH_PASS |
| 1-8 | LEFT, TOP_LEFT, TOP, TOP_RIGHT, RIGHT, BOTTOM_RIGHT, BOTTOM, BOTTOM_LEFT | 11 | SHORT_PASS |
| 9 | LONG_PASS | 12 | SHOT |
| 13 | SPRINT | 14 | RELEASE_DIRECTION |
| 15 | RELEASE_SPRINT | 16 | SLIDING |
| 17 | DRIBBLE | 18 | RELEASE_DRIBBLE |

Directions, sprint and dribble stay on until released. Passes and shots go the way the player faces,
so turn first and kick on the next step (the sample `agent.py` does this).

## Beyond rules

Training a model (reinforcement learning with the Gymnasium API) is allowed: see the full guide,
written by `codepraxis-football init guide` to `guide/README.md`.
