from santas_little_helpers import day, get_data, timed
from santas_little_classes import Point
from santas_little_utils import build_dict_map, neighbours

today = day(2022, 23)

attempt_move = [
  lambda p: (p.n.t, {p.n, p.nw, p.ne}),
  lambda p: (p.s.t, {p.s, p.sw, p.se}),
  lambda p: (p.w.t, {p.w, p.nw, p.sw}),
  lambda p: (p.e.t, {p.e, p.ne, p.se})
]


def empty_ground(cave):
  min_x = min(x for x, _ in cave)
  min_y = min(y for _, y in cave)
  max_x = max(x for x, _ in cave)+1
  max_y = max(y for _, y in cave)+1
  return len(range(min_x, max_x)) * len(range(min_y, max_y)) - len(cave)


def plant_seedlings(cave, checkpoints=[10]):
  t = 0
  while True:
    if t in checkpoints:
      yield empty_ground(cave)
    try_move = dict()
    n_cave = set()
    for elf in cave:
      p = Point(*elf)
      ns = set(neighbours(elf, cave))
      if len(ns) == 0:
        n_cave.add(elf)
        continue
      for o in range(4):
        i = (t + o) % 4
        target, test = attempt_move[i](p)
        if all(pd.t not in ns for pd in test):
          try_move[elf] = target
          break
      else:
        n_cave.add(elf)
    if len(try_move) == 0:
      yield t+1
    for cur, n_pos in try_move.items():
      others = {t_pos for other, t_pos in try_move.items() if cur != other}
      unique = n_pos not in others
      n_cave.add(n_pos if unique else cur)
    cave = n_cave
    t += 1


def part2(inp):
  for x in inp:
    print(x)
  return None


def parse(line):
  return line


def main():
  inp = list(get_data(today))
  cave_scan, _ = build_dict_map(inp, criteria='#')
  cave = set(cave_scan.keys())
  star_gen = plant_seedlings(cave)
  print(f'{today} star 1 = {next(star_gen)}')
  print(f'{today} star 2 = {next(star_gen)}')


if __name__ == '__main__':
  timed(main)
