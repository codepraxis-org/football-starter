# All commands

Run them from inside `football-starter`. The pattern: what to do, the agent, the game mode.

```sh
codepraxis-football play round1/finisher.py                        # you play, with the keyboard
codepraxis-football watch agent.py round2/match_5v5.py             # watch the agent, live window
codepraxis-football eval agent.py round1/dribbler.py --episodes 50 # score one mode (JSON)
codepraxis-football video agent.py round2/match_5v5.py --view topdown -o match.mp4
codepraxis-football watch-match agent.py random final/match_11v11.py   # two agents, live
codepraxis-football match agent.py other.py final/match_11v11.py       # two agents, no window
codepraxis-football levels                                         # the game's built-in modes
```

- `random` and `idle` work in place of an agent file. `builtin` (the game's own AI playing your
  player) works in `watch` and `eval`, not in two-agent commands.
- Keyboard in `play` (click the window first): arrows move, hold `e` sprint, hold `c` dribble,
  `s` short pass, `a` high pass, `w` long pass, `d` shoot, `x` slide tackle, `Esc` quit.
- `--fast` skips the pauses after goals and set pieces in the window and videos.
- `eval`, the round scripts and top-down videos are exact: same seed, same result. The 3D window and
  3D videos run extra engine code, so a match there can play out differently from the scored one.
