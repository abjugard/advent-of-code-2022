from santas_little_helpers import day, get_data, timed
from santas_little_utils import neighbours

today = day(2022, 9)


def distance(x, y, x_t, y_t):
  return abs(x-x_t), abs(y-y_t)


def next_t(p, p_t):
  ns = list(neighbours(p_t))
  if p in ns or p == p_t:
    return p_t
  d_min = 10
  p_min = None
  for pd in ns:
    dx, dy = distance(*p, *pd)
    if dx > 1 or dy > 1:
      continue
    d = dx + dy
    if d < d_min:
      d_min = d
      p_min = pd
    if d == 1:
      return p_min
  return p_min


def predict_rope(inp, rope_length=2):
  head, *rope = [(0, 0)]*rope_length
  visited = set([head])
  for xd, yd, n in inp:
    for _ in range(n):
      x, y = head
      x += xd
      y += yd
      head = (x, y)
      for idx in range(len(rope)):
        rope[idx] = next_t((x, y), rope[idx])
        x, y = rope[idx]
      visited.add(rope[-1])
  return len(visited)


def offset(d):
  if d == 'L':
    return (-1, 0)
  if d == 'R':
    return (1, 0)
  if d == 'U':
    return (0, 1)
  if d == 'D':
    return (0, -1)


def parse(line):
  d, n = line.split(' ')
  return *offset(d), int(n)


def main():
  inp = list(get_data(today, [('func', parse)]))
  print(f'{today} star 1 = {predict_rope(inp)}')
  print(f'{today} star 2 = {predict_rope(inp, rope_length=10)}')


if __name__ == '__main__':
  timed(main)
