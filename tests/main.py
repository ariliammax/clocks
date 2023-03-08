# main.py
# in tests

from clocks.common.config import Config
from clocks.machine.main import MessageQueue
from clocks.machine.main import main as machine_main
from threading import Thread

import pytest


# some "mocks" of the machines/sockets.
# purely because shutting off sockets is annoying.
class DummyMachine(object):
    def __init__(self, name=''):
        self._name = name
        self._out = []
        self.message_queue = MessageQueue()

    def sendall(self, data: bytes):
        self._out.append(data)
        self.message_queue.append(int.from_bytes(data, byteorder='little'))


# some "mocks" of a file.
# so we can easily run tests on the output logs.
class DummyLog(object):
    class Message(object):
        def __init__(self, event, time, length, clock_t):
            self.event = event
            self.time = float(time)
            self.length = int(length)
            self.clock_t = int(clock_t)

        def __str__(self):
            return Config.DELIMITER.join([
                f'{self.event!s}',
                f'{self.time!s}',
                f'{self.length!s}',
                f'{self.clock_t!s}'])

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

    def flush(self):
        pass

    def write(self, msg):
        params = msg.split(Config.DELIMITER)
        self._logs.append(DummyLog.Message(*params))


# ONTO THE TESTS


class Help:
    @staticmethod
    def wrap_random_seq(seq):
        return lambda: (seq.pop(0) if len(seq) == 0 else None)

    @staticmethod
    def generate_asserts(per_assert):
        return [lambda machines, logs: per_assert(machines[i], logs[i])
                for i in range(3)]

    @staticmethod
    def assert_internal_t(t):
        def assert_internal(machine, logs):
            return logs[t].event == Config.MSG_INTERNAL
        return assert_internal

    @staticmethod
    def assert_clock_t_eq(t, t2):
        def assert_clock(machine, logs):
            return logs[t].clock_t == t2
        return assert_clock

    @staticmethod
    def assert_no_messages(machine, logs):
        return len(machine.message_queue) == 0


@pytest.mark.skip('The big mama test... shouldn\'t parametrize this bad mama')
def test_machines_logs(max_steps,
                       durations_s=[0.1, 0.1, 0.1],
                       random_gens=[lambda: 4,
                                    lambda: 4,
                                    lambda: 4],
                       assertions=[]):
    machines = [DummyMachine() for _ in range(3)]
    logs = [DummyLog() for _ in range(3)]
    machine_threads = \
        [Thread(target=machine_main,
                kwargs=dict(duration_s=durations_s[i],
                            log=logs[i],
                            max_steps=max_steps,
                            message_queue=machine.message_queue,
                            other_sockets=(machines[:i] +
                                           machines[i + 1:],
                                           ),
                            random_gen=random_gens[i]))
         for i, machine in enumerate(machines)]
    [thread.start() for thread in machine_threads]
    [thread.join() for thread in machine_threads]

    for assertion in assertions:
        assert assertion(machines, logs)


@pytest.mark.parametrize('max_steps', [1, 2])
def test_simple_peer(max_steps):
    test_machines_logs(
        max_steps,
        assertions=(Help.generate_asserts(Help.assert_internal_t(0)) +
                    Help.generate_asserts(Help.assert_clock_t_eq(0, 1)) +
                    Help.generate_asserts(Help.assert_no_messages)))
