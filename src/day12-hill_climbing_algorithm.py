from santas_little_helpers import day, get_data, timed
from santas_little_utils import build_dict_map, neighbours
import networkx as nx

today = day(2022, 12)
G = nx.DiGraph()


def distance_to_hill(start, target):
  return nx.shortest_path_length(G, start, target)


def calculate_best_start(low_positions, target):
  return min(nx.shortest_path_length(G, p, target) for p in low_positions)


def construct_graph(m):
  d, _ = build_dict_map(m, conv_func=ord)
  low_positions = []

  for p, value in d.items():
    if value == ord('S'): start, value = p, ord('a')
    if value == ord('E'): target, value = p, ord('z')

    ns = list(neighbours(p, d, diagonals=False))

    if value == ord('a'):
      if any(d[n] == ord('b') for n in ns):
        low_positions.append(p)

    for n in ns:
      n_value = d[n]
      if n_value <= value + 1:
        G.add_edge(p, n)

  return start, target, low_positions


def main():
  start, target, low_positions = construct_graph(get_data(today))
  print(f'{today} star 1 = {distance_to_hill(start, target)}')
  print(f'{today} star 2 = {calculate_best_start(low_positions, target)}')


if __name__ == '__main__':
  timed(main)
