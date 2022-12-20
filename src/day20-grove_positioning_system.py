from santas_little_helpers import day, get_data, timed
from dataclasses import dataclass

today = day(2022, 20)


@dataclass
class Coordinate:
  value: int = 0
  idx: int = 0

  def __add(self, other):
    return self.value + other.value
  def __radd__(self, other):
    return other + self.value


def find_by_index(l, original_index):
  for idx, node in enumerate(l):
    if node.idx == original_index:
      return node, idx


def find_by_value(l, value):
  for idx, node in enumerate(l):
    if node.value == value:
      return node, idx


def get_pos(l, idx):
  target = idx % len(l)
  if target == 0:
    target = len(l)
  return target


def mix(file):
  for i in range(len(file)):
    chunk, pos = find_by_index(file, i)
    file = file[:pos] + file[pos+1:]
    target = get_pos(file, pos + chunk)
    file.insert(target, chunk)

  return file


def decrypt(file, decryption_key=1, times=1):
  file = [Coordinate(value*decryption_key, idx) for idx, value in enumerate(file)]
  for _ in range(times):
    file = mix(file)
  _, zero = find_by_value(file, 0)
  return sum(file[get_pos(file, zero+offset)] for offset in [1000, 2000, 3000])


def main():
  file = list(get_data(today, [('func', int)]))
  print(f'{today} star 1 = {decrypt(file)}')
  print(f'{today} star 2 = {decrypt(file, decryption_key=811589153, times=10)}')


if __name__ == '__main__':
  timed(main)
