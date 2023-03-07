# main.py
# in clocks.system

from clocks.common.config import Config
from clocks.machine.main import start
from multiprocessing import Process


if __name__ == "__main__":
    for i in range(3):
        p = Process(
            target=start,
            kwargs=dict(machine_address=Config.MACHINES[i],
                        other_machine_addresses=(Config.MACHINES[:i] +
                                                 Config.MACHINES[i + 1:])))
        p.daemon = True
        p.start()
    while True:
        pass
