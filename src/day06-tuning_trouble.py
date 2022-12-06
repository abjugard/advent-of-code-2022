from santas_little_helpers import day, get_data, timed

today = day(2022, 6)


def parse_packet_stream(stream, buffer_size=4):
  for idx in range(buffer_size, len(stream)):
    buffer = stream[idx-buffer_size:idx]
    if len(set(buffer)) == buffer_size:
      return idx


def main():
  stream = list(next(get_data(today)))
  print(f'{today} star 1 = {parse_packet_stream(stream)}')
  print(f'{today} star 2 = {parse_packet_stream(stream, buffer_size=14)}')


if __name__ == '__main__':
  timed(main)
