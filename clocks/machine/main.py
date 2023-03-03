# main.py
# in clocks.machine

from clocks.common.config import Config
from random import randint
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
from time import sleep, time
from typing import Callable, List, Tuple


def logical_step(duration_s: float = 0.0,
                 **kwargs):
    start_t_s = time()
    roll_die(**kwargs)
    remaining_s = -(time() - start_t_s)
    logical_steps_taken = 0
    while remaining_s < 0:
        # if it is more than a step, make it
        # an integral number of steps
        remaining_s += duration_s
        logical_steps_taken += 1
    sleep(remaining_s)
    return logical_steps_taken


def roll_die(logical_clock_time, message_queue, other_sockets):
    if len(message_queue) == 0:
        r = 3  # randint(1, 10)
        # 8 since 8*8=64 i.e. long
        data = logical_clock_time.to_bytes(Config.INT_LEN, byteorder='little')
        match r:
            case 1:
                other_sockets[0].sendall(data)
            case 2:
                other_sockets[1].sendall(data)
            case 3:
                other_sockets[0].sendall(data)
                other_sockets[1].sendall(data)
            case _:
                return
    else:
        message = message_queue.pop()


def accept_clients(s: socket, other_machine_addresses):
    print(s)
    for _ in other_machine_addresses:
        s.settimeout(Config.TIMEOUT)
        s.accept()
        s.settimeout(None)


def listen_to_clients(s: socket, message_queue):
    sleep(Config.TIMEOUT)
    print(s)
    while True:
        response = s.recv(1024)  # Config.INT_LEN)
        logical_clock_time = int.from_bytes(response, Config.INT_LEN, byteorder='little')
        print(logical_clock_time)
        message_queue.append(logical_clock_time)


def handler(e, s: socket = None):
    s.close()
    if e is not None:
        print('error')
        raise e


def start(handler: Callable = handler,
          machine_address: Tuple = (),
          other_machine_addresses: List[Tuple] = []):
    s = socket(AF_INET, SOCK_STREAM)
    try:
        s.bind(machine_address)
        s.listen()
        sleep(Config.TIMEOUT)
        message_queue = []
        Thread(target=accept_clients,
                args=(s, other_machine_addresses)).start()
        other_sockets = []
        for other_machine_address in other_machine_addresses:
            other_socket = socket(AF_INET, SOCK_STREAM)
            other_socket.connect(other_machine_address)
            other_sockets.append(other_socket)
        Thread(target=listen_to_clients,
                args=(s, message_queue)).start()
        r = randint(1, 6)
        logical_clock_time = 0
        while True:  # logical_clock_time < 1:
            logical_clock_time += (
                logical_step(duration_s=(1 / r),
                                logical_clock_time=logical_clock_time,
                                message_queue=message_queue,
                                other_sockets=other_sockets)
            )
    except Exception as e:
        handler(e, s)
    finally:
        handler(None, s=s)
    

if __name__ == "__main__":
    start()
