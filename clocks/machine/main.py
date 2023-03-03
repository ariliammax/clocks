# main.py
# in clocks.machine

from random import randint
from time import sleep, time
from typing import Callable


def logical_step(target: Callable = None,
                 duration_s: float = 0.0,
                 **kwargs):
    start_t_s = time()
    ret = target(**kwargs)
    remaining_s = -(time() - start_t_s)
    while remaining_s < 0:
        # if it is more than a step, make it
        # an integral number of steps
        remaining_s += duration_s
    sleep(remaining_s)
    return ret


def start():
    r = randint(1, 6)
    while True:
        logical_step(target=lambda: print(r),
                     duration_s=(1 / r))


if __name__ == "__main__":
    start()
