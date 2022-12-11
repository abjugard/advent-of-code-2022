from santas_little_helpers import day, get_data, timed
from collections import deque
from operator import mul, add
from copy import deepcopy

today = day(2022, 11)
monkeys = []


def monkey_business(items, modulo=None, rounds=20):
  inspections = [0]*len(monkeys)

  for _ in range(rounds):
    for idx, op, value, mod, t_choice, f_choice in monkeys:
      monkey_items = items[idx]
      inspections[idx] += len(monkey_items)
      for _ in range(len(monkey_items)):
        item = monkey_items.popleft()

        argument = item if value is None else value
        item = op(item, argument)

        if modulo is not None:
          item %= modulo
        else:
          item //= 3

        outcome = item % mod == 0
        choice = t_choice if outcome else f_choice
        items[choice].append(item)

  return mul(*sorted(inspections, reverse=True)[:2])


def parse(inp):
  items = dict()
  modulo = 1

  for idx, m_it in enumerate(inp):
    next(m_it) # skip first line
    raw_items = next(m_it).split(':')[1]
    items[idx] = deque(map(int, raw_items.split(',')))

    op, argument = next(m_it).split()[-2:]
    op = mul if op == '*' else add
    value = None if argument == 'old' else int(argument)

    mod = int(next(m_it).split()[-1])
    t_choice, f_choice = int(next(m_it)[-1]), int(next(m_it)[-1])

    monkeys.append((idx, op, value, mod, t_choice, f_choice))

    modulo *= mod
  return items, modulo


def main():
  items, modulo = parse(get_data(today, groups=True))
  print(f'{today} star 1 = {monkey_business(deepcopy(items))}')
  print(f'{today} star 2 = {monkey_business(items, modulo, rounds=10000)}')


if __name__ == '__main__':
  timed(main)
