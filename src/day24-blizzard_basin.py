from santas_little_helpers import day, get_data, timed
from santas_little_classes import Point, Origo
from santas_little_utils import build_dict_map

today = day(2022, 24)


blizzard_dirs = {
  '^': Origo.n,
  '>': Origo.e,
  '<': Origo.w,
  'v': Origo.s
}


def get_next(p, d):
  np = p + d
  if   np.x > w-2: np.x = 1
  elif np.x < 1:   np.x = w-2
  elif np.y > h-2: np.y = 1
  elif np.y < 1:   np.y = h-2
  return np, d


def update_blizzards(blizzards):
  n_blizzards = set()
  for blizzard in blizzards:
    n_blizzards.add(get_next(*blizzard))
  return n_blizzards


def update_alternatives(alternatives, blizzards):
  n_alternatives = set()
  for p in alternatives:
    n_alternatives.update((p.direct_neighbours & field) - blizzards)
  return n_alternatives


def traverse_field(blizzards, start, goal):
  target = goal
  alternatives = set([start])

  t = 0
  while True:
    blizzards = update_blizzards(blizzards)
    blizzard_ps = set(p for p, _ in blizzards)
    alternatives = update_alternatives(alternatives, blizzard_ps)
    if target in alternatives:
      if target == goal:
        yield t + 1
      alternatives = set([target])
      target = start if target == goal else goal
    t += 1


def parse_blizzards(field):
  blizzards = set((Point(*p), c) for p, c in field.items() if c not in '#.')
  n_blizzards = set()
  for p, c in blizzards:
    d = blizzard_dirs[c]
    n_blizzards.add((p, d))
  return n_blizzards


def parse(initial_scan):
  global w, h, field

  field, (w, h) = build_dict_map(initial_scan)
  blizzards = parse_blizzards(field)
  field = set(Point(*p) for p, c in field.items() if c != '#')

  start = next(p.x for p in field if p.y == 0)
  goal = next(p.x for p in field if p.y == h-1)

  return blizzards, Point(start, 0), Point(goal, h-1)


def main():
  blizzards, start, goal = parse(get_data(today))

  star_gen = traverse_field(blizzards, start, goal)
  print(f'{today} star 1 = {next(star_gen)}')
  print(f'{today} star 2 = {next(star_gen)}')


if __name__ == '__main__':
  timed(main)
