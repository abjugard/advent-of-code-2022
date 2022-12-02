from santas_little_helpers import day, get_data, timed

today = day(2022, 1)


def most_snacks(groups, redundancy=1):
  return sum(groups[:redundancy])


def main():
  inp = get_data(today, [('func', int)], groups=True)
  groups = sorted([sum(group) for group in inp], reverse=True)
  print(f'{today} star 1 = {most_snacks(groups)}')
  print(f'{today} star 2 = {most_snacks(groups, 3)}')


if __name__ == '__main__':
  timed(main)
