from santas_little_helpers import day, get_data, timed
from collections import defaultdict
from itertools import pairwise
import re

today = day(2022, 14)
cave = set()


def neighbours(x, y):
  yield x, y+1
  yield x-1, y+1
  yield x+1, y+1


def simulate_sand(height, flow_origin):
  count = 0
  star1 = None
  while flow_origin not in cave:
    p = flow_origin
    while True:
      pn = next((n for n in neighbours(*p) if n not in cave), None)
      if pn is None:
        cave.add(p)
        count += 1
        break
      p = pn
      if star1 is None and p[1] == height:
        star1 = count
        yield star1
  yield count


def populate_cave(line):
  parts = line.split(' -> ')
  for l, r in pairwise(parts):
    l_x, l_y = map(int, l.split(','))
    r_x, r_y = map(int, r.split(','))
    start_x, start_y = min(l_x, r_x), min(l_y, r_y)
    end_x, end_y = max(l_x, r_x), max(l_y, r_y)

    for x in range(start_x, end_x + 1):
      for y in range(start_y, end_y + 1):
        cave.add((x, y))


def main():
  list(get_data(today, [('func', populate_cave)]))
  height = max(p[1] for p in cave)

  for x in range(-1000, 1000):
    cave.add((x, height + 2))

  star_gen = simulate_sand(height, (500, 0))
  print(f'{today} star 1 = {next(star_gen)}')
  print(f'{today} star 2 = {next(star_gen)}')


if __name__ == '__main__':
  timed(main)
