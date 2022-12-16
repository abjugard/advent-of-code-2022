from santas_little_helpers import day, get_data, timed
from santas_little_classes import Point
import re

today = day(2022, 15)
sensor_re = re.compile(r'Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)')


def dont_locate_distress_beacon(target_y=2_000_000):
  seen = set()
  beacons = set()

  for sensor, beacon, radius in sensors:
    if beacon.y == target_y:
      beacons.add(beacon.x)
    row_radius = radius-abs(target_y-sensor.y)
    if row_radius < 0:
      continue
    seen.update(range(sensor.x-row_radius, sensor.x+row_radius+1))

  return len(seen-beacons)


def locate_distress_beacon(min_y=0, max_y=4_000_000):
  for y in range(min_y, max_y+1):
    x_ranges = []
    for sensor, _, radius in sensors:
      row_radius = radius-abs(sensor.y-y)
      if row_radius < 0:
        continue
      x_ranges.append((sensor.x-row_radius, sensor.x+row_radius))

    contiguous_ranges = []
    (start, end), *x_ranges = sorted(x_ranges)
    for next_start, next_end in x_ranges:
      if end >= next_start:
        end = max(end, next_end)
      else:
        contiguous_ranges.append((start, end))
        start, end = next_start, next_end
    contiguous_ranges.append((start, end))

    if len(contiguous_ranges) == 2:
      (_, high), *_ = contiguous_ranges
      x = high + 1
      return x*max_y + y


def parse(line):
  s_x, s_y, b_x, b_y = map(int, sensor_re.match(line).groups())
  sensor = Point(s_x, s_y)
  beacon = Point(b_x, b_y)
  return sensor, beacon, sensor.manhattan_distance_to(beacon)


def main():
  global sensors
  sensors = list(get_data(today, [('func', parse)]))
  print(f'{today} star 1 = {dont_locate_distress_beacon()}')
  print(f'{today} star 2 = {locate_distress_beacon()}')


if __name__ == '__main__':
  timed(main)
