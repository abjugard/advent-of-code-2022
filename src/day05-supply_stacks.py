from santas_little_helpers import day, get_data, timed
from santas_little_utils import transpose
from collections import deque
from copy import deepcopy
import re

today = day(2022, 5)
instructions_re = re.compile(r'move ([\d]+) from ([\d]+) to ([\d]+)')


def move_crates(crates, instructions, reverse=False):
  for count, start_col, dest_col in instructions:
    stack = [crates[start_col].popleft() for _ in range(count)]
    if reverse:
      stack.reverse()
    crates[dest_col].extendleft(stack)
  return ''.join(head for head, *_ in crates.values())


def parse_crates(crates):
  crates = transpose(crates)
  result = dict()
  for i in range(1, len(crates), 4):
    *stack, stack_id = crates[i]
    result[int(stack_id)] = deque(''.join(stack).strip())
  return result


def parse_instructions(instructions):
  for instr in instructions:
    count, start_col, dest_col = instructions_re.match(instr).groups()
    yield (int(count), int(start_col), int(dest_col))


def main():
  crates, instr = get_data(today, groups=True)
  crates = parse_crates(crates)
  instr = list(parse_instructions(instr))
  print(f'{today} star 1 = {move_crates(deepcopy(crates), instr)}')
  print(f'{today} star 2 = {move_crates(crates, instr, reverse=True)}')


if __name__ == '__main__':
  timed(main)
