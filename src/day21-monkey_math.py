from santas_little_helpers import day, get_data, timed
import operator
import sympy

today = day(2022, 21)


def part1(inp):
  known = dict()
  for idx, data in inp:
    if len(data) == 1:
      known[idx] = data[0]

  ops = [(idx, data) for idx, data in inp if len(data) > 1]

  while 'root' not in known:
    for idx, (left, op, right) in ops:
      if idx not in known and left in known and right in known:
        known[idx] = op(known[left], known[right])

  return int(known['root'])


def part2(inp):
  lookup = dict()
  humn = sympy.Symbol('humn')

  def solve_rec(monkey):
    args = lookup[monkey]
    if monkey == 'humn':
      return humn
    if len(args) == 1:
      return args[0]

    left, op, right = lookup[monkey]
    return op(solve_rec(left), solve_rec(right))

  for idx, args in inp:
    lookup[idx] = args

  left, _, right = lookup['root']

  left = solve_rec(left)
  right = solve_rec(right)

  root = sympy.solve(left - right)

  return int(root[0])


def get_operator(op):
  if op == '+':
    return operator.add
  elif op == '*':
    return operator.mul
  elif op == '-':
    return operator.sub
  elif op == '/':
    return operator.truediv


def parse(line):
  idx, data = line.split(': ')
  if data.isnumeric():
    return idx, [int(data)]

  left, op, right = data.split(' ')
  return idx, [left, get_operator(op), right]


def main():
  inp = list(get_data(today, [('func', parse)]))
  print(f'{today} star 1 = {part1(inp)}')
  print(f'{today} star 2 = {part2(inp)}')


if __name__ == '__main__':
  timed(main)
