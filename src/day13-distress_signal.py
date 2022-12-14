from santas_little_helpers import day, get_data, timed
from santas_little_utils import mul, flatten
from itertools import zip_longest
from functools import cmp_to_key
import json

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


Packet = cmp_to_key(compare)


def packets_in_order(packets):
  return sum(idx + 1 for idx, (a, b) in enumerate(packets) if a < b)


def sort_and_search(packets, *divider_packets):
  divider_packets = list(map(Packet, divider_packets))

  packets = flatten(packets)
  packets.extend(divider_packets)
  packets.sort()

  def search():
    for idx, packet in enumerate(packets):
      if packet in divider_packets:
        yield idx + 1

  return mul(search())


def main():
  packets = get_data(today, [('func', json.loads), ('func', Packet)], groups=True)
  packets = [list(grp) for grp in packets]
  print(f'{today} star 1 = {packets_in_order(packets)}')
  print(f'{today} star 2 = {sort_and_search(packets, [[2]], [[6]])}')


if __name__ == '__main__':
  timed(main)
