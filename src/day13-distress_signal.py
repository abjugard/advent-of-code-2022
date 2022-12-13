from santas_little_helpers import day, get_data, timed
from santas_little_utils import mul
from itertools import zip_longest
from functools import cmp_to_key

today = day(2022, 13)


def compare(l, r):
  l_t, r_t = type(l), type(r)
  if l_t is int and r_t is int:
    return l-r
  if l_t is int: 
    l = [l]
  if r_t is int: 
    r = [r]
  for i_l, i_r in zip_longest(l, r, fillvalue=None):
    if i_l is None:
      return -1
    if i_r is None:
      return 1
    res = compare(i_l, i_r)
    if res != 0:
      return res
  return 0


def packets_in_order(inp):
  return sum(idx + 1 for idx, pair in enumerate(inp) if compare(*pair) < 0)


def sort_and_search(inp, *divider_packets):
  packets = [item for grp in inp for item in grp]
  packets.extend(divider_packets)

  packets = sorted(packets, key=cmp_to_key(compare))

  def search():
    keys = [str(p) for p in packets]
    to_find = [str(p) for p in divider_packets]
    for idx, key in enumerate(keys):
      if key in to_find:
        yield idx + 1

  return mul(search())


def main():
  inp = list(get_data(today, [('func', eval)], groups=True))
  inp = [list(grp) for grp in inp]
  print(f'{today} star 1 = {packets_in_order(inp)}')
  print(f'{today} star 2 = {sort_and_search(inp, [[2]], [[6]])}')


if __name__ == '__main__':
  timed(main)
