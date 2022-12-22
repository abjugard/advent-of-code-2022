from santas_little_helpers import day, get_data, timed
from santas_little_utils import build_dict_map
import re

today = day(2022, 22)

instrs_re = re.compile(r'([\d]+)([\w])')

dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

from_bot = lambda p: (p[0],  p[1]-1)
from_top = lambda p: (p[0],  p[1]+1)
invert_y = lambda p: (p[0], -p[1]-1)
rotate   = lambda p: (p[1],  p[0]  )

# this solution will only work if 
# your input is shaped as follows:
#            ____
#           |1|2|
#          _|3|‾
#         |5|4|
#         |6|‾
#          ‾‾

sec_fold = {
# <section> <dir> <turns> <offset> <point mapping function>
  (1, 0): { (-1,  0): ('RR', (-1,  2), invert_y),   # 1 -> 5
            ( 0, -1): ('R',  (-1,  3), rotate  )},  # 1 -> 6
  (2, 0): { ( 0,  1): ('R',  (-1,  1), rotate  ),   # 2 -> 3
            ( 1,  0): ('RR', (-1,  2), invert_y),   # 2 -> 4
            ( 0, -1): ('',   (-2,  3), from_bot)},  # 2 -> 6
  (1, 1): { ( 1,  0): ('L',  ( 1, -1), rotate  ),   # 3 -> 2
            (-1,  0): ('L',  (-1,  1), rotate  )},  # 3 -> 5
  (1, 2): { ( 1,  0): ('RR', ( 1, -2), invert_y),   # 4 -> 2
            ( 0,  1): ('R',  (-1,  1), rotate  )},  # 4 -> 6
  (0, 2): { (-1,  0): ('RR', ( 1, -2), invert_y),   # 5 -> 1
            ( 0, -1): ('R',  ( 1, -1), rotate  )},  # 5 -> 3
  (0, 3): { (-1,  0): ('L',  ( 1, -3), rotate  ),   # 6 -> 1
            ( 0,  1): ('',   ( 2, -3), from_top),   # 6 -> 2
            ( 1,  0): ('L',  ( 1, -1), rotate  )}   # 6 -> 4
}


def turn(direction, turn):
  if turn == None:
    return direction
  idx = dirs.index(direction)
  offset = -1 if turn == 'L' else 1
  return dirs[(idx+offset) % len(dirs)]


def flat_move(pos, direction, backoff=None):
  x, y = pos
  xd, yd = direction
  n_pos = (x+xd) % w, (y+yd) % h
  c = at_pos(n_pos)
  if c == '.':
    return direction, n_pos
  if backoff is None:
    backoff = direction, pos
  if c == '#':
    return backoff
  else:
    return flat_move(n_pos, direction, backoff)


def fold(pos, direction):
  x, y = pos

  x_s, y_s = sec = x // sec_length, y // sec_length

  turns, (xd_s, yd_s), func = sec_fold[sec][direction]
  x_base, y_base = (x_s+xd_s)*sec_length, (y_s+yd_s)*sec_length

  n_x, n_y = func((x, y))
  n_pos = x_base + n_x % sec_length, y_base + n_y % sec_length

  for d in turns:
    direction = turn(direction, d)

  return n_pos, direction


def at_pos(pos):
  return board[pos] if pos in board else None


def cube_move(pos, direction):
  x, y = pos

  xd, yd = n_direction = direction
  n_pos = x+xd, y+yd
  if n_pos not in board:
    n_pos, n_direction = fold(pos, direction)
  c = board[n_pos]
  if c == '.':
    return n_direction, n_pos
  if c == '#':
    return direction, pos


def parse_map(instrs, move_fn=flat_move):
  x = min(x for x, y in board if y == 0)
  pos = (x, 0)
  direction = (1, 0)
  for count, d in instrs:
    for _ in range(count):
      direction, n_pos = move_fn(pos, direction)
      if n_pos == pos:
        break
      pos = n_pos
    direction = turn(direction, d)
  x, y = pos
  return 1000*(y + 1) + 4*(x + 1) + dirs.index(direction)


def parse(line):
  for match in instrs_re.findall(line + 'F'):
    count, d = match
    yield int(count), d if d != 'F' else None


def main():
  global board, w, h, sec_length
  board, instrs = get_data(today, groups=True)
  board, (w, h) = build_dict_map(board, criteria='.#')
  sec_length = min(x for x, y in board if y == 0)
  instrs = list(parse(next(instrs)))
  print(f'{today} star 1 = {parse_map(instrs)}')
  print(f'{today} star 2 = {parse_map(instrs, move_fn=cube_move)}')


if __name__ == '__main__':
  timed(main)
