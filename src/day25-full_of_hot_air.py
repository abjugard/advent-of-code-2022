from santas_little_helpers import day, get_data, timed

today = day(2022, 25)


def to_base_n_parts(base_10, base=5):
  base_5_parts = []
  while base_10 > 0:
    base_10, remainder = divmod(base_10, base)
    base_5_parts.insert(0, remainder)
  return base_5_parts


def to_snafu_parts(base_5_parts):
  snafu_parts = base_5_parts.copy()
  while any(part > 2 for part in snafu_parts):
    if snafu_parts[0] > 2:
      snafu_parts.insert(0, 0)
    non_snafus = [idx for idx, part in enumerate(snafu_parts) if part > 2]
    for idx in non_snafus:
      snafu_parts[idx-1] += 1
      snafu_parts[idx]   -= 5
  while snafu_parts[0] == 0:
    del snafu_parts[0]
  return snafu_parts


def int2snafu(base_10):
  base_5_parts = to_base_n_parts(base_10)
  snafu_parts = to_snafu_parts(base_5_parts)

  snafu = ''
  for snafu_part in snafu_parts:
    if snafu_part >= 0:
      snafu += str(snafu_part)
    else:
      snafu += '-' if snafu_part == -1 else '='

  assert snafu2int(snafu) == base_10
  return snafu


snafu_mult = { '2': 2, '1': 1, '0': 0, '-': -1, '=': -2 }
def snafu2int(snafu):
  s = 0
  for magnitude, snafu_c in enumerate(reversed(snafu)):
    base_5 = '1' + '0'*magnitude
    base_10 = int(base_5, 5)
    s += snafu_mult[snafu_c] * base_10
  return s


def main():
  base_10_sum = sum(get_data(today, [('func', snafu2int)]))
  print(f'{today} star 1 = {int2snafu(base_10_sum)}')
  print(f'{today} star 2 = Merry Christmas!')


if __name__ == '__main__':
  timed(main)
