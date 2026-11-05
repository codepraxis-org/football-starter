"""Runs an agent through a round's modes, headless and in parallel, and says PASS or FAIL.

Used by run_round1.py and run_round2.py; you don't run this file yourself.
"""

import concurrent.futures
import dataclasses
import os
import sys
import time

SEED = 1000           # practice seeds; final judging uses the same modes with seeds you haven't seen
STATUS_EVERY = 3.0    # seconds between progress lines


@dataclasses.dataclass
class Mode:
  title: str
  file: str           # the game mode (a level file next to this script)
  episodes: int
  metric: str         # at least target: 'goal_rate', 'win_rate', 'goal_diff' (a match); at most: 'concede_rate'
  target: float
  chunk: int = 10     # episodes per job; small = smoother progress and better use of CPU cores


def run_round(title, modes, must_pass, argv=None):
  import argparse
  here = os.path.dirname(os.path.abspath(__file__))
  p = argparse.ArgumentParser(description=f'Run {title} on your agent.')
  p.add_argument('agent', nargs='?', default='agent.py')
  p.add_argument('--only', type=int, metavar='N', help='run only mode N')
  p.add_argument('--quick', action='store_true', help='a quarter of the episodes: faster, noisier')
  p.add_argument('--workers', type=int, default=max(1, (os.cpu_count() or 2) - 1))
  args = p.parse_args(argv)
  builtin = args.agent in ('builtin', 'random', 'idle')  # the game's own players, for comparison
  agent = args.agent if builtin else os.path.abspath(args.agent)
  if not builtin and not os.path.exists(agent):
    sys.exit(f'agent file not found: {args.agent} (run this from the folder with your agent.py)')

  chosen = [(no, m) for no, m in enumerate(modes, 1) if not args.only or args.only == no]
  print(f'{title}: {os.path.basename(agent)}, {len(chosen)} mode(s), {args.workers} parallel workers',
        flush=True)
  for no, m in chosen:
    print(f'  {no}. {m.title:<12} {m.file:<22} {_episodes(m, args.quick):>3} episodes  '
          f'pass: {_target_text(m)}', flush=True)
  print(flush=True)

  jobs, results = {}, {no: [] for no, _ in chosen}
  started = time.time()
  with concurrent.futures.ProcessPoolExecutor(args.workers) as pool:
    for no, m in chosen:
      level = os.path.join(here, m.file)
      n = _episodes(m, args.quick)
      for first in range(0, n, m.chunk):
        size = min(m.chunk, n - first)
        jobs[pool.submit(_run_chunk, agent, level, SEED + first, size)] = no
    pending, passed, last_status = set(jobs), 0, time.time()
    while pending:
      done, pending = concurrent.futures.wait(pending, timeout=STATUS_EVERY,
                                              return_when=concurrent.futures.FIRST_COMPLETED)
      for job in done:
        no = jobs[job]
        try:
          results[no].extend(job.result())
        except Exception as e:  # noqa: BLE001 - the engine or the level file, not the agent
          sys.exit(f'mode {no} could not run: {type(e).__name__}: {e}')
        m = dict(chosen)[no]
        if len(results[no]) == _episodes(m, args.quick):
          ok, line = _verdict(m, results[no])
          passed += ok
          print(f"  {no}. {m.title:<12} {'PASS' if ok else 'FAIL'}  {line}", flush=True)
      if pending and time.time() - last_status >= STATUS_EVERY:
        last_status = time.time()
        running = [f'{dict(chosen)[no].title} {len(r)}/{_episodes(dict(chosen)[no], args.quick)}'
                   for no, r in results.items() if len(r) < _episodes(dict(chosen)[no], args.quick)]
        print(f'     ... {time.time() - started:.0f}s  running: ' + ', '.join(running), flush=True)

  errors = sum(1 for r in results.values() for e in r if e['error'])
  timeouts = sum(e['timeouts'] for r in results.values() for e in r)
  if errors or timeouts:
    first = next(e['error'] for r in results.values() for e in r if e['error']) if errors else ''
    print(f'\n  note: {errors} episode(s) ended by an error in your agent, {timeouts} step(s) slower '
          f'than 50 ms (played as IDLE)' + (f'\n  first error: {first}' if first else ''))
  needed = len(chosen) if args.only else must_pass
  verdict = 'PASSED' if passed >= needed else 'NOT PASSED'
  print(f'\n{title}: {passed}/{len(chosen)} modes passed, {needed} needed -> {verdict}'
        f'  ({time.time() - started:.0f}s)')
  if args.quick:
    print('(--quick: fewer episodes. Run without it for the full check.)')
  return passed >= needed


def _run_chunk(agent, level, seed, episodes):
  from codepraxis_football.evaluate import evaluate
  return evaluate(agent, level, episodes=episodes, seed=seed)['results']


def _episodes(mode, quick):
  return max(2, mode.episodes // 4) if quick else mode.episodes


def _target_text(m):
  if m.metric == 'goal_rate':
    return f'score in {m.target:.0%} of attempts'
  if m.metric == 'win_rate':
    return f'win {m.target:.0%} of matches'
  if m.metric == 'goal_diff':
    return f'win by {m.target:g}+ goals a match on average'
  return f'concede in at most {m.target:.0%} of attempts'


def _verdict(m, results):
  n = len(results)
  scored = sum(r['goals_for'] > 0 for r in results)
  conceded = sum(r['goals_against'] > 0 for r in results)
  wins = sum(r['goals_for'] > r['goals_against'] for r in results)
  losses = sum(r['goals_for'] < r['goals_against'] for r in results)
  goals = f"{sum(r['goals_for'] for r in results)}-{sum(r['goals_against'] for r in results)}"
  if m.metric == 'goal_rate':
    return scored / n >= m.target, f'scored in {scored}/{n} = {scored / n:.0%}  (need {m.target:.0%})'
  if m.metric == 'goal_diff':
    diff = sum(r['goals_for'] - r['goals_against'] for r in results) / n
    return (diff >= m.target,
            f'won {wins}, drew {n - wins - losses}, lost {losses} of {n}, goals {goals} = {diff:+.2f} a match'
            f'  (need {m.target:+g})')
  if m.metric == 'win_rate':
    return (wins / n >= m.target,
            f'won {wins}, drew {n - wins - losses}, lost {losses} of {n}, goals {goals}  (need {m.target:.0%} wins)')
  return (conceded / n <= m.target,
          f'conceded in {conceded}/{n} = {conceded / n:.0%}  (need at most {m.target:.0%})')
