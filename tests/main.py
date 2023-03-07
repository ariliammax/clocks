# main.py
# in tests

from clocks.common.config import Config
from clocks.machine.main import MessageQueue
from clocks.machine.main import main as machine_main
from clocks.machine.main import logical_step
from threading import Thread

import pytest


class DummyMachine(object):
    def __init__(self, name=''):
        self._name = name
        self._out = []
        self.message_queue = MessageQueue()

    def sendall(self, data: bytes):
        self._out.append(data)
        self.message_queue.append(int.from_bytes(data, byteorder='little'))


class DummyLog(object):
    class Message(object):
        def __init__(self, event, time, length, clock_t):
            self.event = event
            self.time = float(time)
            self.length = int(length)
            self.clock_t = int(clock_t)

        def __str__(self):
            return (f'{self.event!s} | {self.time!s} | '
                    f'{self.length!s} | {self.clock_t!s}'
                    .replace(' | ', Config.DELIMITER))

    def __init__(self, name=''):
        self._name = name
        self._logs = []

    def __getitem__(self, key):
        return self._logs[key]

    def __len__(self):
        return len(self._logs)

    def __str__(self):
        return '\n'.join([str(msg)
                          for msg in self._logs])

    def write(self, msg):
        params = msg.split(Config.DELIMITER)
        self._logs.append(DummyLog.Message(*params))


@pytest.mark.parametrize('max_steps', [1, 2])
def test_simple_peer(max_steps):
    machines = [DummyMachine() for _ in range(3)]
    logs = [DummyLog() for _ in range(3)]
    machine_threads = \
        [Thread(target=machine_main,
                kwargs=dict(log=logs[i],
                            max_steps=max_steps,
                            message_queue=machine.message_queue,
                            other_sockets=(machines[:i] +
                                           machines[i + 1:]),
                            duration_s=0.1))
         for i, machine in enumerate(machines)]
    [thread.start() for thread in machine_threads]
    [thread.join() for thread in machine_threads]

    # make sure that all the first log messages are logical clock time 1.
    # but check the negation, so that if it fails we can see the stringified
    # log outputs of the failing ones
    assert(len({i: str(log) for i, log in enumerate(logs)
                if len(log) > 0 and
                log[0].clock_t != 1}) == 0)
