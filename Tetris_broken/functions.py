from settings import *
from classes import Button
import sys
selected_button = None

def get_record():
    try:
        with open('record.txt') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record.txt', 'w') as f:
            f.write('0')

def set_record(record, score):
    try:
        rec = max(int(record), score)
    except ValueError:
        rec = score
    with open('record.txt', 'w') as f:
        f.write(str(rec))

def quitGame():
  pygame.quit()
  sys.exit()

