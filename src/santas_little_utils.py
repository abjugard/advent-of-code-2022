from collections import deque
from santas_little_helpers import alphabet

directions_8 = [(-1, -1), (0, -1), (1, -1),
                (-1,  0),          (1,  0),
                (-1,  1), (0,  1), (1,  1)]

directions_4 = [(0, -1), (-1, 0), (1, 0), (0, 1)]


def get_iterator(variable):
  try:
    it = iter(variable)
    return it
  except TypeError:
    return get_iterator([variable])


def skip(count, it):
  for _ in range(count):
    next(it)
  return next(it)


def get_last(generator):
  d = deque(generator, maxlen=2)
  d.pop()
  return d.pop()


def tesseract_parse(inp, lookup=True, chars=alphabet.upper()):
  from santas_little_ocr_lib import parse_datastructure, set_to_grid, create_image
  data, boundary = parse_datastructure(inp, lookup)
  try:
    import pytesseract
    image = create_image(data, *boundary)
    return pytesseract.image_to_string(image, config=f'--psm 6 -c tessedit_char_whitelist={chars}').strip()
  except ImportError:
    for line in set_to_grid(data, *boundary):
      print(''.join('█' if c else ' ' for c in line))
    print('for cooler results, please install Pillow and pytesseract\n' \
        + '(along with a tesseract-ocr distribution)')
    return None


def build_dict_map(map_data, conv_func=None, criteria=None):
  the_map = dict()
  def get_value(c):
    return c if conv_func is None else conv_func(c)
  h, w = 0, 0
  for y, xs in enumerate(map_data):
    for x, c in enumerate(xs):
      if criteria is None or c in criteria:
        the_map[(x, y)] = get_value(c)
      w = max(w, x)
    h = max(h, y)
  return the_map, (w+1, h+1)


def neighbours(p, borders=None, diagonals=True):
  def within_borders(p_n, borders):
    if borders is None:
      return True
    elif isinstance(borders, dict):
      return p_n in borders
    elif isinstance(borders, set):
      return p_n in borders
    elif isinstance(borders, list):
      x_n, y_n = p_n
      h = len(borders)
      return h > 0 and 0 <= y_n < h and 0 <= x_n < len(borders[0])
    raise Exception(f'unknown datastructure: {type(borders)}')
  x, y = p
  for xd, yd in directions_8 if diagonals else directions_4:
    p_n = x + xd, y + yd
    if within_borders(p_n, borders):
      yield p_n


def mul(numbers):
  result = 1
  for n in numbers:
    if n == 0:
      return 0
    result *= n
  return result


def transpose(l):
  return list(map(list, zip(*l)))


def flatten(list_of_lists):
  return [item for l in list_of_lists for item in l]
