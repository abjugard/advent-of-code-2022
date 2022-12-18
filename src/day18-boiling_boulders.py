from santas_little_helpers import day, get_data, timed
from dataclasses import dataclass

today = day(2022, 18)


@dataclass
class Point:
  x: int = 0
  y: int = 0
  z: int = 0


  def __lt__(self, other):
    return self.x < other.x or self.y < other.y or self.z < other.z
  def __hash__(self):
    return 2971215073 * self.x + 433494437 * self.y + 479001599 * self.z


  @property
  def neighbours(self):
    neighbours = set()
    neighbours.add(Point(self.x+1, self.y,   self.z  ))
    neighbours.add(Point(self.x-1, self.y,   self.z  ))
    neighbours.add(Point(self.x,   self.y+1, self.z  ))
    neighbours.add(Point(self.x,   self.y-1, self.z  ))
    neighbours.add(Point(self.x,   self.y,   self.z+1))
    neighbours.add(Point(self.x,   self.y,   self.z-1))
    return neighbours


  def clear(self, others):
    return sum(1 for n in self.neighbours if n not in others)


  def covered(self, others):
    return sum(1 for n in self.neighbours if n in others)


def exterior_surface_area(lava_droplet):
  max_x = max(p.x for p in lava_droplet)
  max_y = max(p.y for p in lava_droplet)
  max_z = max(p.z for p in lava_droplet)

  minimum = Point(-1, -1, -1)
  maximum = Point(max_x + 1, max_y + 1, max_z + 1)

  to_check = [Point(0, 0, 0)]
  seen = set()
  while to_check:
    p = to_check.pop()
    if p in seen or p < minimum or p > maximum:
      continue
    yield p.covered(lava_droplet)
    seen.add(p)
    to_check.extend(p.neighbours - lava_droplet)


def main():
  inp = get_data(today, [('split', ','), ('map', int)])
  lava_droplet = set([Point(*p) for p in inp])
  print(f'{today} star 1 = {sum(c.clear(lava_droplet) for c in lava_droplet)}')
  print(f'{today} star 2 = {sum(exterior_surface_area(lava_droplet))}')


if __name__ == '__main__':
  timed(main)
