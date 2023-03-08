# main.py
# in clocks.system

from clocks.common.config import Config
from clocks.machine.main import start
from multiprocessing import Process


def main():
    for i in range(3):
        p = Process(
            target=start,
            kwargs=dict(duration_s=Config.DURATIONS[i],
                        machine_address=Config.MACHINES[i],
                        other_machine_addresses=(Config.MACHINES[:i] +
                                                 Config.MACHINES[i + 1:])))
        p.start()
    while True:
        pass

if __name__ == "__main__":
    main()
