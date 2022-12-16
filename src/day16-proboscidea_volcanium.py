from santas_little_helpers import day, get_data, timed
from functools import cache
import re

today = day(2022, 16)
valve_re = re.compile(r'Valve ([\w]+) has flow rate=([\d]+); tunnel[s]* lead[s]* to valve[s]* ([\w, ]+)')
flow_rate = dict()
tunnels = dict()


@cache
def open_valves(valve, time_left, valves_open):
  if time_left == 0:
    return 0, valves_open

  best = 0, valves_open
  time_left -= 1
  
  pressure = flow_rate[valve] * time_left
  n_valves_open = tuple(sorted(valves_open + (valve,)))
  for node in tunnels[valve]:
    if pressure > 0 and valve not in valves_open:
      i_pressure, i_valves_open = open_valves(node, time_left-1, n_valves_open)
      best = max(best, (pressure + i_pressure, i_valves_open))
    best = max(best, open_valves(node, time_left, valves_open))

  return best


def parallelise(n=2):
  pressure, valves_open = open_valves('AA', 26, ())
  for _ in range(n-1):
    pressure_n, valves_open = open_valves('AA', 26, valves_open)
    pressure += pressure_n
  return pressure


def parse(line):
  valve, valve_flow_rate, valve_tunnels = valve_re.match(line).groups()
  flow_rate[valve] = int(valve_flow_rate)
  tunnels[valve] = valve_tunnels.split(', ')


def main():
  list(get_data(today, [('func', parse)]))
  print(f'{today} star 1 = {open_valves("AA", 30, ())[0]}')
  print(f'{today} star 2 = {parallelise(n=2)}')


if __name__ == '__main__':
  timed(main)
