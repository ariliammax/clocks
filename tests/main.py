# main.py
# in tests

from random import randint
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
        return lambda:(seq.pop(0) if len(seq) != 0 else None)

    @staticmethod
    def generate_assert(machine_idx, per_assert):
        return [lambda machines, logs: per_assert(machines[machine_idx], logs[machine_idx])]

    @staticmethod
    def generate_asserts(per_assert):
        return [lambda machines, logs: per_assert(machines[i], logs[i])
                for i in range(3)]
    
    @staticmethod
    def generate_assert_all_equal(f):
        return [lambda machines, logs: all(f(m, l) == f(machines[0], logs[0]) 
                for m, l in zip(machines, logs))]
    
    @staticmethod
    def generate_assert_ascending_order(f):
        return [lambda machines, logs: all(
            f(m, l) <= f(machines[i+1], logs[i+1])
            for i, (m, l) in enumerate(zip(machines[:-1], logs[:-1]))
        )]
    
    @staticmethod
    def get_num_logs(machine, logs):
        return len(logs)

    @staticmethod
    def assert_internal_t(t):
        def assert_internal(machine, logs):
            return logs[t].event == Config.MSG_INTERNAL
        return assert_internal
    
    @staticmethod
    def assert_send_one_t(t):
        def assert_one(machine, logs):
            return logs[t].event == Config.MSG_SEND_0
        return assert_one

    @staticmethod
    def assert_send_other_t(t):
        def assert_other(machine, logs):
            return logs[t].event == Config.MSG_SEND_1
        return assert_other

    @staticmethod
    def assert_send_both_t(t):
        def assert_both(machine, logs):
            return logs[t].event == Config.MSG_SEND_01
        return assert_both

    @staticmethod
    def assert_clock_t_eq(t, t2):
        def assert_clock(machine, logs):
            return logs[t].clock_t == t2
        return assert_clock

    @staticmethod
    def assert_clock_t_gte(t, t2):
        def assert_clock(machine, logs):
            return logs[t].clock_t >= t2
        return assert_clock

    @staticmethod
    def assert_no_messages(machine, logs):
        return len(machine.message_queue) == 0

    @staticmethod
    def true_random():
        yield randint(1, Config.RANDOM_EVENT)
    
    @staticmethod
    def send_one():
        return 1

    @staticmethod
    def send_other():
        return 2

    @staticmethod
    def send_both():
        return 3

    @staticmethod
    def internal_event():
        return 4

    @staticmethod
    def get_last_logical_clock_val(machine, logs):
        return logs[len(logs) - 1].clock_t




@pytest.mark.skip()
def test_machines_logs(max_steps,
                       durations_s=[0.1, 0.1, 0.1],
                       message_queues=[MessageQueue(),
                                       MessageQueue(),
                                       MessageQueue()],
                       random_gens=[Help.internal_event,
                                    Help.internal_event,
                                    Help.internal_event],
                       assertions=[]):
    machines = [DummyMachine() for _ in range(3)]
    logs = [DummyLog() for _ in range(3)]
    machine_threads = \
        [Thread(target=machine_main,
                kwargs=dict(duration_s=durations_s[i],
                            log=logs[i],
                            max_steps=max_steps,
                            message_queue=message_queues[i],
                            other_sockets=machines[:i] + machines[i + 1:],
                            random_gen=random_gens[i]))
         for i, machine in enumerate(machines)]
    [thread.start() for thread in machine_threads]
    [thread.join() for thread in machine_threads]

    for assertion in assertions:
        assert assertion(machines, logs)


# @pytest.mark.parametrize('max_steps', [1, 2])
# def test_simple_peer(max_steps):
#     test_machines_logs(
#         max_steps,
#         assertions=(Help.generate_asserts(Help.assert_internal_t(0)) +
#                     Help.generate_asserts(Help.assert_clock_t_eq(0, 1)) +
#                     Help.generate_asserts(Help.assert_no_messages)))


# @pytest.mark.parametrize('max_steps', [1])
# def test_pull_and_update_from_message_queue(max_steps):
#      test_machines_logs(
#         max_steps,
#         message_queues=[MessageQueue([15]), MessageQueue(), MessageQueue()],
#         assertions=(Help.generate_assert(0, Help.assert_clock_t_eq(0, 16)) + 
#                     Help.generate_asserts(Help.assert_no_messages)))


# @pytest.mark.parametrize('max_steps', [2])
# def test_update_logical_clock(max_steps):
#      test_machines_logs(
#         max_steps,
#         message_queues=[MessageQueue([15, 2]), MessageQueue(), MessageQueue()],
#         assertions=(Help.generate_assert(0, Help.assert_clock_t_eq(1, 17))))
        

# @pytest.mark.parametrize('max_steps', [2])
# def test_message_queue_precedence(max_steps):
#      test_machines_logs(
#         max_steps,
#         random_gens=[Help.send_both,
#                      Help.internal_event,
#                      Help.internal_event],
#         message_queues=[MessageQueue([15, 30]), MessageQueue(), MessageQueue()],
#         assertions=(Help.generate_assert(0, Help.assert_clock_t_eq(1, 31)) +
#                     Help.generate_assert(1, Help.assert_clock_t_eq(1, 2)) + 
#                     Help.generate_assert(2, Help.assert_clock_t_eq(1, 2))))


# @pytest.mark.parametrize('max_steps', [3])
# def test_send_both(max_steps):
#     test_machines_logs(
#         max_steps,
#         durations_s=[0.1, 0.15, 0.15],
#         message_queues=[MessageQueue([15]), MessageQueue(), MessageQueue()],
#         random_gens=[Help.wrap_random_seq([Help.send_both, Help.internal_event]),
#                      Help.internal_event,
#                      Help.internal_event],
#         assertions=(Help.generate_assert(0, Help.assert_send_both_t(1)) +
#                     Help.generate_assert_all_equal(Help.get_last_logical_clock_val)) +
#                     Help.generate_asserts(Help.assert_no_messages))

# @pytest.mark.parametrize('max_steps', [3])
# def test_send_one(max_steps):
#     test_machines_logs(
#         max_steps,
#         durations_s=[0.1, 0.15, 0.15],
#         message_queues=[MessageQueue([15]), MessageQueue(), MessageQueue()],
#         random_gens=[Help.wrap_random_seq([Help.send_one, Help.internal_event]),
#                      Help.internal_event,
#                      Help.internal_event],
#         assertions=(Help.generate_assert(0, Help.assert_send_one_t(1))))

@pytest.mark.parametrize('max_steps', [3])
def test_send_other(max_steps):
    test_machines_logs(
        max_steps,
        durations_s=[0.1, 0.18, 0.15],
        message_queues=[MessageQueue([15]), MessageQueue(), MessageQueue()],
        random_gens=[Help.wrap_random_seq([Help.send_one, Help.internal_event]),
                     Help.internal_event,
                     Help.internal_event],
        assertions=(Help.generate_assert(0, Help.assert_clock_t_eq(2, 18)) +
                    Help.generate_assert(1, Help.assert_clock_t_eq(2, 18)) + 
                    Help.generate_assert(2, Help.assert_clock_t_eq(2, 3))))
    

# @pytest.mark.parametrize('max_steps', [15, 30, 45])
# def test_same_duration(max_steps):
#     test_machines_logs(
#         max_steps,
#         random_gens=[Help.true_random,
#                      Help.true_random,
#                      Help.true_random],
#         assertions=(Help.generate_assert_all_equal(Help.get_num_logs) +
#                     Help.generate_assert_all_equal(Help.get_last_logical_clock_val))
#     )


# @pytest.mark.parametrize('max_steps', [15, 30, 45])
# def test_ascending_durations(max_steps):
#     test_machines_logs(
#         max_steps,
#         durations_s=[0.3, 0.2, 0.1],
#         random_gens=[Help.internal_event,
#                      Help.internal_event,
#                      Help.internal_event],
#         assertions=(Help.generate_assert_ascending_order(Help.get_num_logs) +
#                     Help.generate_assert_ascending_order(Help.get_last_logical_clock_val))
#     )
