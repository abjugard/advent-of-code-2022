from santas_little_helpers import day, get_data, timed
from santas_little_classes import Point, Origo

today = day(2022, 9)


def simulate_motion(head, tail):
  if tail.is_neighbour(head):
    return tail
  return min(tail.neighbours, key=lambda p: p.manhattan_distance_to(head))


def simulate_rope(motions, rope_length=2):
  first_node, *rope = [Point() for _ in range(rope_length)]
  visited = set([first_node])

  for vector, count in motions:
    for _ in range(count):
      first_node += vector
      next_node = first_node
      for idx in range(len(rope)):
        next_node = rope[idx] = simulate_motion(next_node, rope[idx])
      visited.add(rope[-1])

  return len(visited)


def vector(d):
  if d == 'U': return Origo.n
  if d == 'R': return Origo.e
  if d == 'D': return Origo.s
  if d == 'L': return Origo.w


def parse(line):
  d, n = line.split(' ')
  return vector(d), int(n)


def main():
  motions = list(get_data(today, [('func', parse)]))
  print(f'{today} star 1 = {simulate_rope(motions)}')
  print(f'{today} star 2 = {simulate_rope(motions, rope_length=10)}')


if __name__ == '__main__':
  timed(main)
