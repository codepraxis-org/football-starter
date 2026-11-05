# Game modes

Every mode is a small Python file with `LEVEL = Level(...)`: `round1/`, `round2/`, `final/`, and
`match_5v5.py` for free play. Copy one to make your own practice mode; use the file anywhere a mode
goes (`codepraxis-football watch agent.py my_mode.py`).

| Setting | Meaning |
|---|---|
| `our_players`, `their_players` | `(x, y, role)` per player. Our goalkeeper is added unless listed |
| `ball` | Where the ball starts |
| `opponent_difficulty` | The built-in AI playing the other team: 0 (stands still) to 1 (strongest) |
| `teammate_difficulty` | The built-in AI playing our players you don't control (default 1) |
| `time_limit` | Steps; 10 steps = 1 second of game time |
| `end_on_goal`, `end_on_ball_out`, `end_on_lost_possession` | End the attempt then (drills) or play on (matches) |
| `offsides` | Offside rule on or off |
| `opponent` | `Team('Rivals', 'green', 'black')` (`from codepraxis_football.teams import Team`): the other team's name and kit; looks only |

Pass marks live in `run_round1.py` and `run_round2.py` (`MODES`). Judging uses the same modes and
marks with seeds you haven't seen.
