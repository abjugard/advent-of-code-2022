from santas_little_helpers import day, get_data, timed
from santas_little_utils import build_dict_map, directions_4, mul
from itertools import product

today = day(2022, 8)

def visibility(comparison, x, y, xd, yd, depth=False):
  pd = x-xd, y-yd
  if pd not in forest:
    return 0 if depth else True
  if comparison <= forest[pd]:
    return 1 if depth else False
  inner = visibility(comparison, *pd, xd, yd, depth)
  return (inner + 1) if depth else inner


def is_visible(p):
  tree_height = forest[p]
  return any(visibility(tree_height, *p, *d) for d in directions_4)


def trees_visible():
  return sum(is_visible(p) for p in forest)


def scenic_score(p):
  tree_height = forest[p]
  return mul(visibility(tree_height, *p, *d, depth=True) for d in directions_4)


def most_scenic_tree():
  return max(scenic_score(p) for p in product(range(1, h), range(1, w)))


def main():
  global forest, w, h
  forest, (w, h) = build_dict_map(get_data(today), conv_func=int)
  print(f'{today} star 1 = {trees_visible()}')
  print(f'{today} star 2 = {most_scenic_tree()}')


if __name__ == '__main__':
  timed(main)
