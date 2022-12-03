from santas_little_helpers import day, get_data, timed, full_alphabet

today = day(2022, 3)


def priority(item):
  return full_alphabet.index(item) + 1


def find_misplaced_items(bags):
  s = 0
  for b in bags:
    l = len(b)//2
    common = set(b[:l]) & set(b[l:])
    s += priority(common.pop())
  return s


def chunks(bags):
  for i in range(0, len(bags), 3):
    yield [set(b) for b in bags[i:i + 3]]


def find_badge(bags):
  s = 0
  for b1, b2, b3 in chunks(bags):
    common = b1 & b2 & b3
    s += priority(common.pop())
  return s


def main():
  bags = list(get_data(today))
  print(f'{today} star 1 = {find_misplaced_items(bags)}')
  print(f'{today} star 2 = {find_badge(bags)}')


if __name__ == '__main__':
  timed(main)
