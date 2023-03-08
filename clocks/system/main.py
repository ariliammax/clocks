# main.py
# in clocks.system

from clocks.common.config import Config
from clocks.machine.main import start
from multiprocessing import Process


def main(durations=Config.DURATIONS,
         ports=None,
         random_event=Config.RANDOM_EVENT):
    machines = Config.MACHINES
    if ports is not None:
        for i in range(len(machines)):
            machines[i] = (machines[i][0], ports[i])
    for i in range(3):
        p = Process(
            target=start,
            kwargs=dict(duration_s=durations[i],
                        machine_address=machines[i],
                        other_machine_addresses=(machines[:i] +
                                                 machines[i + 1:]),
                        random_event=random_event))
        p.start()
    while True:
        pass


if __name__ == "__main__":
    main()
