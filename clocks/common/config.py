# config.py
# in clocks.common


class Config:
    DURATIONS = [None, None, None]
    DELIMITER = ","
    FIGURES = "figures/"
    INT_LEN = 8
    LOGS = "logs/"
    # (HOST, PORT)
    MACHINES = [('localhost', 10000),
                ('localhost', 20000),
                ('localhost', 30000)]
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
