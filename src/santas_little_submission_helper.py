import json, re, importlib, sys, os
from time import sleep
from datetime import date, datetime
from pathlib import Path
from typing import Callable, Iterator
from santas_little_helpers import aoc_root, config
from io import StringIO

aoc_submission_history = aoc_root / '.submission-history'
aoc_response_time_re = re.compile(r'You have ((?P<minutes>[\d]+)m |)(?P<seconds>[\d]+)s left to wait.')
standard_answer_re = re.compile(r'([\d]{4}-[\d]{2}-[\d]{2}) star ([\d]{1}) = (.+)')


def get_submission_history(today: date, level: int):
  if not aoc_submission_history.exists():
    aoc_submission_history.mkdir()
  
  file_path = aoc_submission_history / f'day{today.day:02}.{str(level)}.json'
  if not file_path.exists():
    return dict()

  with file_path.open() as f:
    return json.load(f)


def __handle_response__(today: date, answer, level, submission_history, text):
  file_path = aoc_submission_history / f'day{today.day:02}.{str(level)}.json'

  if 'gave an answer too recently' in text:
    match = aoc_response_time_re.search(text)
    minutes = match.group('minutes')
    seconds = 1 + int(match.group('seconds'))
    if minutes is not None:
      seconds += 60 * int(minutes)
    for t in reversed(range(1, seconds)):
      print(f'Throttled, waiting {t} seconds before retry...', end='\r', flush=True)
      sleep(1)
    print()
    return submit_answer(today, answer, level)

  response = {
    'timestamp': datetime.now().isoformat(),
    'success': False
  }

  if 'not the right answer' in text:
    print(f'Wrong answer', end='')
    hint = None
    if 'too high' in text:
      hint = 'too high'
    if 'too low' in text:
      hint = 'too low'
    if 'right answer for someone else' in text:
      hint = 'correct for another player'
    if hint is not None:
      print(f', hint: {hint}')
      response['hint'] = hint
  elif 'the right answer' in text:
    response['success'] = True
    emoji = '⭐️' if level == 1 else '🌟'
    print(f'Correct answer! {emoji}')
  else:
    print(text)

  submission_history[str(answer)] = response
  with file_path.open('w') as f:
    json.dump(submission_history, f, indent=4)


def is_solved(submission_history):
  return any(response['success'] == True for response in submission_history.values())


def import_requests():
  from requests import request, codes
  from bs4 import BeautifulSoup
  return request, codes, BeautifulSoup


def submit_answer(today: date, answer, level: int = 1) -> None:
  if type(answer) not in [str, int]:
    print(f'Ignoring answer of type {type(answer)}, submission must be str or int')
    return
  if answer in ['', 0]:
    print('Ignoring empty answer')
    return
  submission_history = get_submission_history(today, level)
  if is_solved(submission_history):
    print(f'Already solved {today} part {level}')
    return
  if str(answer) in submission_history:
    response = submission_history[str(answer)]
    print(f"Already tried that at {response['timestamp']}", end='')
    if 'hint' in response:
      print(f", hint: {response['hint']}", end='')
    print()
    return

  request, status_codes, BeautifulSoup = import_requests()
  url = f'https://adventofcode.com/{today.year}/day/{today.day}/answer'
  payload = {'level': level, 'answer': answer}
  res = request('POST', url, cookies=config, data=payload)
  with (aoc_root / 'last_response.html').open('wb') as f2:
    f2.write(res.content)

  soup = BeautifulSoup(res.content, 'html.parser')
  content = soup.find_all('article')[0]
  try:
    __handle_response__(today, answer, level, submission_history, content.text)
  except Exception:
    print(content.text)


def redirect_stdout():
  stream = sys.stdout = StringIO()
  return stream


def restore_stdout():
  sys.stdout = sys.__stdout__


def __submit__(day):
  stream = redirect_stdout()
  theday = day.today
  day.main()
  restore_stdout()
  answers = [None, None]
  for line in stream.getvalue().strip().split('\n'):
    match = standard_answer_re.match(line)
    if match is None:
      print('Day not formatted using standard format')
      print(line)
      continue
    found_date, level, answer = match.groups()
    assert(found_date == str(theday))
    answers[int(level)-1] = answer
  assert(all(answer is not None for answer in answers))
  for idx in range(2):
    level = idx + 1
    print(f'{theday} star {level}, submitting "{answers[idx]}"')
    submit_answer(theday, answer, level)
    sleep(6) # there's flood protection between levels


def __submit_all__():
  for t in reversed(range(1, 6)):
    print(f'About to run and submit all days in {t} seconds...', end='\r', flush=True)
    sleep(1)
  print()
  for file in sorted(Path('.').glob('day[!X]?-*.py')):
    if 'day25' in file.name:
      exit()
    try:
      day = importlib.import_module(file.name[:-3])
    except Exception as e:
      print(f'Failed to import \'{file.name}\': {e}', file=sys.stderr)
      print()
      continue
    print(f'Running \'{file.name}\':')
    __submit__(day)
    print()


if __name__ == '__main__':
  __submit_all__()
