# main.py
# in clocks.system

from clocks.machine.main import start
from multiprocessing import Process


if __name__ == "__main__":
    for _ in range(3):
        Process(target=start).start()
