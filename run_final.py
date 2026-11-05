"""Final: two agents play 11 vs 11 against each other.

    python run_final.py agent.py other_agent.py               # headless: 4 matches, about a minute
    python run_final.py agent.py other_agent.py --matches 8   # more matches, a fairer result
    python run_final.py agent.py other_agent.py --watch       # watch one match live (5 minutes)
    python run_final.py agent.py agent.py                     # no opponent yet? play yourself

Sides swap every match, so neither agent profits from the side it starts on. Each agent sees
the pitch as if attacking right, so the same agent.py works on either side.
Winner: more matches won, then goal difference.
"""

import argparse
import concurrent.futures
import os
import sys
import time

LEVEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'final', 'match_11v11.py')
SEED = 2000  # practice seeds; the real final uses seeds nobody has seen


def main():
  p = argparse.ArgumentParser(description='Two agents play 11 vs 11.')
  p.add_argument('agent_a')
  p.add_argument('agent_b')
  p.add_argument('--matches', type=int, default=4, help='headless: how many matches (even is fairest)')
  p.add_argument('--watch', action='store_true', help='play one match live in a window')
  p.add_argument('--fps', type=int, default=10, help='--watch speed: 10 = real time, 20 = double')
  p.add_argument('--workers', type=int, default=max(1, (os.cpu_count() or 2) - 1))
  args = p.parse_args()
  for path in (args.agent_a, args.agent_b):
    if not os.path.exists(path):
      sys.exit(f'agent file not found: {path} (run this from the folder with your agents)')
  a, b = os.path.abspath(args.agent_a), os.path.abspath(args.agent_b)
  name_a, name_b = _team_name(a), _team_name(b)
  if name_a == name_b:  # e.g. an agent against itself
    name_a, name_b = f'{name_a} (A)', f'{name_b} (B)'
  print(f'Final, 11 vs 11: {name_a} ({args.agent_a}) vs {name_b} ({args.agent_b})', flush=True)

  if args.watch:
    from codepraxis_football import viewer
    print('Opening the game window (Esc or close it to stop) ...', flush=True)
    info = viewer.watch_match(a, b, LEVEL, fps=args.fps, seed=SEED, episodes=1)
    goals_a, goals_b = info['score']
    print(f'\nFull time: {name_a} {goals_a} - {goals_b} {name_b}')
    return

  print(f'{args.matches} matches, sides swap each match, {args.workers} parallel workers\n', flush=True)
  started = time.time()
  results = {}
  with concurrent.futures.ProcessPoolExecutor(min(args.workers, args.matches)) as pool:
    jobs = {pool.submit(_play, a, b, SEED + i, swapped=i % 2 == 1): i for i in range(args.matches)}
    pending = set(jobs)
    while pending:
      done, pending = concurrent.futures.wait(pending, timeout=5,
                                              return_when=concurrent.futures.FIRST_COMPLETED)
      for job in done:
        i = jobs[job]
        goals_a, goals_b, note = job.result()
        results[i] = (goals_a, goals_b)
        left = name_b if i % 2 else name_a
        winner = name_a if goals_a > goals_b else name_b if goals_b > goals_a else 'draw'
        print(f'  match {i + 1}: {name_a} {goals_a} - {goals_b} {name_b}   ({left} kicked off on the left; '
              f'{winner if winner == "draw" else winner + " wins"}){note}', flush=True)
      if pending:
        print(f'     ... {time.time() - started:.0f}s, {len(results)}/{args.matches} matches done', flush=True)

  wins_a = sum(ga > gb for ga, gb in results.values())
  wins_b = sum(gb > ga for ga, gb in results.values())
  goals_a = sum(ga for ga, _ in results.values())
  goals_b = sum(gb for _, gb in results.values())
  print(f'\nWon: {name_a} {wins_a}, {name_b} {wins_b}, drawn {args.matches - wins_a - wins_b}. '
        f'Goals {goals_a}-{goals_b}.  ({time.time() - started:.0f}s)')
  if (wins_a, goals_a - goals_b) > (wins_b, goals_b - goals_a):
    print(f'Winner: {name_a}')
  elif (wins_b, goals_b - goals_a) > (wins_a, goals_a - goals_b):
    print(f'Winner: {name_b}')
  else:
    print('Level on wins and goal difference: play more matches (--matches 8).')


def _play(a, b, seed, swapped):
  """One match; returns (goals of a, goals of b, note on errors)."""
  from codepraxis_football.evaluate import match
  r = match(b, a, LEVEL, episodes=1, seed=seed) if swapped else match(a, b, LEVEL, episodes=1, seed=seed)
  m = r['results'][0]
  goals_left, goals_right = m['goals_a'], m['goals_b']
  goals_a, goals_b = (goals_right, goals_left) if swapped else (goals_left, goals_right)
  errors = [e for e in (m.get('error_a'), m.get('error_b')) if e]
  return goals_a, goals_b, f'  [agent error: {errors[0]}]' if errors else ''


def _team_name(path):
  from codepraxis_football.agents import load_agent
  team = load_agent(path).team
  return team.name if team else os.path.splitext(os.path.basename(path))[0]


if __name__ == '__main__':
  main()
