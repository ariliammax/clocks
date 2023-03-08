# main.py
# in experiments

from clocks.common.config import Config
from clocks.system.main import main
from matplotlib import pyplot
from multiprocessing import Process

import pytest


class ExperimentParameters:
    COLUMN_TO_LABEL = {
        2: "message_queue_length",
        3: "logical_clock_time",
    }
    PARAMETERS = [
        # [NAME, DURATIONS, INTERNAL_PROBABILITY, PORTS]
        ["A1", [1/6, 1/6, 1/6], 10, [10001, 20001, 30001]],
        ["A2", [1/6, 1, 1], 10, [10002, 20002, 30002]],
        ["A3", [1/6, 1/6, 1], 10, [10003, 20003, 30003]],
        ["A4", [1/6, 1/2, 1], 10, [10004, 20004, 30004]],
        ["A5", [1/6, 1/4, 1/2], 10, [10005, 20005, 30005]],
        ["B1", [1/6, 1/6, 1/6], 4, [10006, 20006, 30006]],
        ["B2", [1/6, 1/5, 1/5], 4, [10007, 20007, 30007]],
        ["B3", [1/6, 1/6, 1/5], 4, [10008, 20008, 30008]],
        ["B4", [1/6, 1/5, 1/4], 4, [10009, 20009, 30009]],
    ]
    TIMEOUT = 5 # 70

@pytest.mark.parametrize("column", [3, 2])
@pytest.mark.parametrize("parameters", ExperimentParameters.PARAMETERS)
def test_experiments(column, parameters):
    # Config.DURATIONS = parameters[1]
    # Config.RANDOM_EVENT = parameters[2]
    # for i in range(len(Config.MACHINES)):
    #     Config.MACHINES[i] = (Config.MACHINES[i][0], parameters[3][i])
    process = Process(target=main)
    process.start()
    process.join(timeout=ExperimentParameters.TIMEOUT)
    process.terminate()
    for i in range(len(Config.MACHINES)):
        machine = Config.MACHINES[i]
        file = open(
            Config.LOGS +
            machine[0] + 
            str(machine[1]) +
            ".txt",
            "r")
        lines = file.readlines()
        print(lines)
        x = []
        y = []
        for line in lines:
            split = line.split(Config.DELIMITER)
            x.append(float(split[1]))
            y.append(int(split[column]))
        file.close()
        pyplot.plot(x, y)
    name = parameters[0]
    label = ExperimentParameters.COLUMN_TO_LABEL[column]
    pyplot.savefig(Config.FIGURES + name + "_" + label + ".png")
    pyplot.close()
