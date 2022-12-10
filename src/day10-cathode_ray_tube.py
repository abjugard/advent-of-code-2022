from santas_little_helpers import day, get_data, timed
from santas_little_utils import tesseract_parse

today = day(2022, 10)


def run_program(inp):
  x = 1
  cycle = signal_strengths = y = 0
  output = set()
  for jump, args in inp:
    for _ in range(jump):
      pos = cycle % 40
      if pos in range(x-1, x+2):
        output.add((pos, y))
      if pos == 39:
        y += 1
      cycle += 1
      if cycle % 40 == 20:
        signal_strengths += cycle * x
    x += args
  return signal_strengths, tesseract_parse(output)


def parse(line):
  if ' ' in line:
    _, argument = line.split(' ')
    return 2, int(argument)
  else:
    return 1, 0


def main():
  inp = get_data(today, [('func', parse)])
  star1, star2 = run_program(inp)
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {star2}')


if __name__ == '__main__':
  timed(main)
