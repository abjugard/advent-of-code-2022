from santas_little_helpers import day, get_data, timed

today = day(2022, 2)


def play(them, us):
  p = us + 1
  if us == them:
    p += 3
  if (them - 2) % 3 == us:
    p += 6
  return p


def play_naively(guide):
  return sum(play(*choices) for choices in guide)


def select(other, desired):
  if desired == 1:
    return other
  return (other + desired - 1) % 3


def play_smartly(guide):
  score = 0
  for them, desired in guide:
    us = select(them, desired)
    score += play(them, us)

  return score


def parse(inp):
  them, us = inp.split(' ')
  return (ord(them)-ord('A'), ord(us)-ord('X'))


def main():
  guide = list(get_data(today, [('func', parse)]))
  print(f'{today} star 1 = {play_naively(guide)}')
  print(f'{today} star 2 = {play_smartly(guide)}')


if __name__ == '__main__':
  timed(main)
