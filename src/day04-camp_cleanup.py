from santas_little_helpers import day, get_data, timed
import re

today = day(2022, 4)
syntax = re.compile(r'([\d]+)-([\d]+),([\d]+)-([\d]+)')


def fully_contained(inp):
  s = 0
  for l, r in inp:
    shared = len(l & r)
    s += shared == len(l) or shared == len(r)
  return s


def overlaps(inp):
  return sum(len(l & r) >= 1 for l, r in inp)


def parse(inp):
  ll, lr, rl, rr = syntax.match(inp).groups()
  l = range(int(ll), int(lr) + 1)
  r = range(int(rl), int(rr) + 1)
  return set(l), set(r)


def main():
  inp = list(get_data(today, [('func', parse)]))
  print(f'{today} star 1 = {fully_contained(inp)}')
  print(f'{today} star 2 = {overlaps(inp)}')


if __name__ == '__main__':
  timed(main)
