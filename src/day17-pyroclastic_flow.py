from santas_little_helpers import day, get_data, timed

today = day(2022, 17)


tower_width = 7
tower = {(x, 0) for x in range(tower_width)}
shapes = [[(2, 0), (3, 0), (4, 0), (5, 0)],
          [(3, 0), (2, 1), (3, 1), (4, 1), (3, 2)],
          [(2, 0), (3, 0), (4, 0), (4, 1), (4, 2)],
          [(2, 0), (2, 1), (2, 2), (2, 3)],
          [(2, 0), (3, 0), (2, 1), (3, 1)]]
jets = None
seen = dict()


def init_shape(shape_id, height):
  shape = shapes[shape_id]
  dy = height + 4
  return [(x, y+dy) for x, y in shape]


def step_shape(shape, jet):
  dx = -1 if jet == '<' else 1

  n_shape = [(x+dx, y) for x, y in shape]
  if any(x < 0 or x >= tower_width or (x, y) in tower for x, y in n_shape):
    n_shape = shape
  shape = n_shape
  n_shape = [(x, y-1) for x, y in shape]
  locked = any(p in tower for p in n_shape)

  return locked, (shape if locked else n_shape)


def calc_shape(jet_idx, shape):
  while True:
    jet = jets[jet_idx]
    jet_idx += 1
    jet_idx %= len(jets)
    locked, shape = step_shape(shape, jet)
    if locked:
      return jet_idx, shape


def cache_key(height):
  magic = 16
  return tuple(sorted([(x, height-y) for x, y in tower if y >= height-magic]))


def play_tetris(checkpoints):
  jet_idx = shape_idx = height = skipped = 0

  while True:
    if shape_idx in checkpoints:
      _, *checkpoints = checkpoints
      yield height + skipped

    shape_id = shape_idx % len(shapes)
    shape = init_shape(shape_id, height)

    jet_idx, shape = calc_shape(jet_idx, shape)

    tower.update(shape)
    height = max(y for _, y in tower)

    key = jet_idx, shape_id, cache_key(height)
    if key in seen:
      p_shape_idx, p_height = seen[key]
      diff_shape_idx = shape_idx-p_shape_idx
      diff_height = height-p_height

      next_checkpoint = int(checkpoints[0])
      multiplier = (next_checkpoint-shape_idx) // diff_shape_idx

      shape_idx += multiplier * diff_shape_idx
      skipped += multiplier * diff_height

    seen[key] = shape_idx, height
    shape_idx += 1


def main():
  global jets
  jets = next(get_data(today))

  star_gen = play_tetris(checkpoints=[2022, 1e12])
  print(f'{today} star 1 = {next(star_gen)}')
  print(f'{today} star 2 = {next(star_gen)}')


if __name__ == '__main__':
  timed(main)
