# config.py
# in clocks.common


class Config:
    INT_LEN = 8
    LOGS = "logs/"
    # (HOST, PORT)
    MACHINES = [('localhost', 11111),
                ('localhost', 22222),
                ('localhost', 33333)]
    RANDOM_CLOCK = 6
    RANDOM_EVENT = 10
    TIMEOUT = 1
