# main.py
# in clocks.machine

from random import randint
from time import sleep


def start():
    r = randint(1, 6)
    while True:
        print(r)
        sleep(1 / r)


if __name__ == "__main__":
    start()
