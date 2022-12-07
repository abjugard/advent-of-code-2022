from santas_little_helpers import day, get_data, timed
from collections import defaultdict

today = day(2022, 7)


def recursive_dir_sizes(fs):
  fs_sizes = defaultdict(lambda: 0)

  for key, value in fs.items():
    cwd_parts = [part for part in key.split('/') if part != '']
    for i in range(len(cwd_parts)):
      cwd = '/' + '/'.join(cwd_parts[:i])
      fs_sizes[cwd] += value

  star1 = sum(v for v in fs_sizes.values() if v <= 100_000)
  return fs_sizes, star1


def delete_large_dir(fs_sizes):
  diskspace = 70_000_000
  required = 30_000_000

  remaining = diskspace-fs_sizes['/']
  target = required-remaining

  for size in sorted(fs_sizes.values()):
    if size >= target:
      return size

  return None


def parse_cmd(line, cwd):
  cwd_parts = [part for part in cwd.split('/') if part != '']

  if 'cd' in line:
    _, cmd, arg = line.split(' ')
    if arg.startswith('/'):
      return arg
    parts = arg.split('/')
    for part in parts:
      if part == '..':
        if len(cwd_parts) > 0:
          cwd_parts.pop()
      else:
        cwd_parts.append(part)

  return '/' + '/'.join(cwd_parts)


def build_fs(it):
  fs = defaultdict(lambda: 0)
  cwd = ''
  for line in it:
    if line.startswith('$'):
      cwd = parse_cmd(line, cwd)
      continue
    size, filename = line.split(' ')
    if size == 'dir':
      continue
    path = '/'.join([cwd, filename])
    fs[path] += int(size)

  return fs


def main():
  fs = build_fs(get_data(today))
  fs_sizes, star1 = recursive_dir_sizes(fs)
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {delete_large_dir(fs_sizes)}')


if __name__ == '__main__':
  timed(main)
