from santas_little_helpers import day, get_data, timed
from santas_little_utils import tesseract_parse

today = day(2022, 10)


def run_vm(program):
  x = 1
  cycle = signal_strengths = 0
  output = set()
  for jump, value in program:
    for _ in range(jump):
      cursor = cycle % 40
      if cursor in range(x-1, x+2):
        output.add((cursor, cycle // 40))
      cycle += 1
      if cycle % 40 == 20:
        signal_strengths += cycle * x
    x += value
  return signal_strengths, tesseract_parse(output)


def parse(line):
  if ' ' in line:
    _, value = line.split(' ')
    return 2, int(value)
  else:
    return 1, 0


def main():
  program = get_data(today, [('func', parse)])
  star1, star2 = run_vm(program)
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {star2}')


if __name__ == '__main__':
  timed(main)
