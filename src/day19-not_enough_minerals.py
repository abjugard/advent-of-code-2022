from santas_little_helpers import day, get_data, timed
from santas_little_utils import mul
import re

today = day(2022, 19)

blueprint_re = re.compile(r'Blueprint ([\d]+): '
   + r'Each ore robot costs ([\d]+) ore. '
   + r'Each clay robot costs ([\d]+) ore. '
   + r'Each obsidian robot costs ([\d]+) ore and ([\d]+) clay. '
   + r'Each geode robot costs ([\d]+) ore and ([\d]+) obsidian.')


def play_starcraft(c_ore, c_cla, c_obs_ore, c_obs_cla, c_geo_ore, c_geo_obs, time_left=24):
  def update_minerals(minerals, ore_d=0, cla_d=0, obs_d=0, geo_d=0):
    ore, cla, obs, geo = minerals
    return ore+ore_d, cla+cla_d, obs+obs_d, geo+geo_d


  def build_robot(minerals, bots, ore=0, cla=0, obs=0, geo=0):
    ore_b, cla_b, obs_b, geo_b = bots
    if ore > 0:
      ore_b += ore
      minerals = update_minerals(minerals, ore_d=-c_ore)
    if cla > 0:
      cla_b += cla
      minerals = update_minerals(minerals, ore_d=-c_cla)
    if obs > 0:
      obs_b += obs
      minerals = update_minerals(minerals, ore_d=-c_obs_ore, cla_d=-c_obs_cla)
    if geo > 0:
      geo_b += geo
      minerals = update_minerals(minerals, ore_d=-c_geo_ore, obs_d=-c_geo_obs)
    return (ore_b, cla_b, obs_b, geo_b), minerals


  def build_target_robot(time_left, target, bots, minerals):
    nonlocal best
    ore_b, cla_b, obs_b, geo_b = bots
    geo = minerals[-1]
    best = max(best, geo)

    # try to smartly exit if we don't think the run will result in a better geode count
    low_potential = sum(range(time_left)) + geo_b * time_left + geo <= best
    if (target == 0 and ore_b >= mc_ore or
        target == 1 and cla_b >= c_obs_cla or
        target == 2 and (obs_b >= c_geo_obs or cla_b == 0) or
        target == 3 and obs_b == 0 or low_potential):
      return

    while time_left > 0:
      ore, cla, obs, geo = minerals
      minerals = update_minerals(minerals, *bots)
      time_left -= 1

      n_b = None
      if target == 0 and ore >= c_ore:
        n_b, n_m = build_robot(minerals, bots, ore=1)
      elif target == 1 and ore >= c_cla:
        n_b, n_m = build_robot(minerals, bots, cla=1)
      elif target == 2 and ore >= c_obs_ore and cla >= c_obs_cla:
        n_b, n_m = build_robot(minerals, bots, obs=1)
      elif target == 3 and ore >= c_geo_ore and obs >= c_geo_obs:
        n_b, n_m = build_robot(minerals, bots, geo=1)
      if n_b is not None:
        for n_target in range(4):
          build_target_robot(time_left, n_target, n_b, n_m)
        return


  best = 0
  mc_ore = max(c_ore, c_cla, c_obs_ore, c_geo_ore)
  bots_init = (1, 0, 0, 0)
  minerals_init = (0, 0, 0, 0)
  for target in range(4):
    build_target_robot(time_left, target, bots_init, minerals_init)

  return best


def part1(blueprints):
  return sum(idx*play_starcraft(*blueprint) for idx, blueprint in blueprints)


def part2(blueprints):
  blueprints = blueprints[:3]
  return mul(play_starcraft(*blueprint, time_left=32) for _, blueprint in blueprints)


def parse(line):
  idx, *blueprint = map(int, blueprint_re.match(line).groups())
  return idx, blueprint


def main():
  blueprints = list(get_data(today, [('func', parse)]))
  print(f'{today} star 1 = {part1(blueprints)}')
  print(f'{today} star 2 = {part2(blueprints)}')


if __name__ == '__main__':
  timed(main)
