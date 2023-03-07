# main.py
# in clocks.machine

from clocks.common.config import Config
from random import randint
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread, RLock
from time import sleep, time
from typing import Callable, List, Tuple

import sys


class MessageQueue(object):
    def __init__(self):
        self._queue = []
        self._lock = RLock()

    def append(self, item):
        with self._lock:
            self._queue.append(item)

    def __len__(self):
        _len = 0
        with self._lock:
            _len = len(self._queue)
        return _len

    def pop(self, idx):
        item = None
        with self._lock:
            try:
                item = self._queue.pop(0)
            except Exception:
                item = None
        return item


def logical_step(duration_s: float,
                 log,
                 logical_clock_time,
                 message_queue,
                 other_sockets):
    start_t_s = time()

    event = ""
    if len(message_queue) == 0:
        r = randint(1, Config.RANDOM_EVENT)
        # 8 since 8*8=64 i.e. long
        data = logical_clock_time.to_bytes(Config.INT_LEN, byteorder='little')
        match r:
            case 1:
                event = "send 0  "
                other_sockets[0].sendall(data)
            case 2:
                event = "send 1  "
                other_sockets[1].sendall(data)
            case 3:
                event = "send 0+1"
                other_sockets[0].sendall(data)
                other_sockets[1].sendall(data)
            case _:
                event = "internal"
    else:
        event = "receive "
        logical_clock_time = max(logical_clock_time, message_queue.pop(0))

    remaining_s = -(time() - start_t_s)
    while remaining_s < 0:
        # if it is more than a step, make it
        # an integral number of steps
        remaining_s += duration_s
        logical_clock_time += 1

    log.write(f'{event!s} | {time()!s} | '
              f'{len(message_queue)!s} | {logical_clock_time!s}'
              .replace(' | ', Config.DELIMITER))

    sleep(remaining_s)
    return logical_clock_time


def accept_clients(message_queue, other_machine_addresses, s: socket):
    for _ in other_machine_addresses:
        connection, _ = s.accept()
        Thread(target=listen_client,
               args=(connection, message_queue)).start()


def listen_client(connection, message_queue):
    while True:
        response = connection.recv(Config.INT_LEN)
        logical_clock_time = int.from_bytes(response, byteorder='little')
        message_queue.append(logical_clock_time)


def handler(e, log, s: socket):
    log.close()
    s.close()
    if e is not None:
        raise e


def start(handler: Callable = handler,
          machine_address: Tuple = (),
          other_machine_addresses: List[Tuple] = [],
          log=None):
    if log is None:
        log = open(
            Config.LOGS +
            machine_address[0] +
            str(machine_address[1]) +
            ".txt",
            "w")
    s = socket(AF_INET, SOCK_STREAM)
    try:
        s.bind(machine_address)
        s.listen()
        s.settimeout(None)
        sleep(Config.TIMEOUT)
        message_queue = MessageQueue()
        Thread(target=accept_clients,
               args=(message_queue, other_machine_addresses, s)).start()
        sleep(Config.TIMEOUT)
        other_sockets = []
        for other_machine_address in other_machine_addresses:
            other_socket = socket(AF_INET, SOCK_STREAM)
            other_socket.connect(other_machine_address)
            other_sockets.append(other_socket)
        duration_s = 1 / randint(1, Config.RANDOM_CLOCK)
        main(handler=handler,
             log=log,
             message_queue=message_queue,
             other_sockets=other_sockets,
             duration_s=duration_s)
    except Exception as e:
        handler(e=e, log=log, s=s)
    finally:
        handler(e=None, log=log, s=s)


def main(handler: Callable = handler,
         log=sys.__stdout__,
         max_steps: int = None,
         message_queue: MessageQueue = None,
         other_sockets: List = [],
         duration_s: float = 1):
    logical_clock_time = 0
    while max_steps is None or logical_clock_time < max_steps:
        logical_clock_time = (
            logical_step(duration_s=duration_s,
                         log=log,
                         logical_clock_time=logical_clock_time,
                         message_queue=message_queue,
                         other_sockets=other_sockets)
        )


if __name__ == "__main__":
    start()
