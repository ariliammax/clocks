# config.py
# in clocks.common


class Config:
    DELIMITER = " | "
    INT_LEN = 8
    LOGS = "logs/"
    # (HOST, PORT)
    MACHINES = [('localhost', 11113),
                ('localhost', 22221),
                ('localhost', 33332)]
    RANDOM_CLOCK = 6
    RANDOM_EVENT = 10
    TIMEOUT = 1

    MSG_INTERNAL = \
        'internal'
    MSG_RECV = \
        'receive '
    MSG_SEND_0 = \
        'send 0  '
    MSG_SEND_1 = \
        'send 1  '
    MSG_SEND_01 = \
        'send 0+1'
