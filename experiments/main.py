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
        # [NAME, DURATIONS, PORTS, RANDOM_EVENT]
        ["A1", [1/6, 1/6, 1/6], [10001, 20001, 30001], 10],
        ["A2", [1/6, 1/1, 1/1], [10002, 20002, 30002], 10],
        ["A3", [1/6, 1/6, 1/1], [10003, 20003, 30003], 10],
        ["A4", [1/6, 1/2, 1/1], [10004, 20004, 30004], 10],
        ["A5", [1/6, 1/4, 1/2], [10005, 20005, 30005], 10],
        ["B1", [1/6, 1/6, 1/6], [10006, 20006, 30006], 4],
        ["B2", [1/6, 1/5, 1/5], [10007, 20007, 30007], 4],
        ["B3", [1/6, 1/6, 1/5], [10008, 20008, 30008], 4],
        ["B4", [1/6, 1/5, 1/4], [10009, 20009, 30009], 4],
    ]
    TIMEOUT = 70

@pytest.mark.parametrize("parameters", ExperimentParameters.PARAMETERS)
def test_experiments(parameters):
    process = Process(target=main, args=parameters[1:])
    process.start()
    process.join(timeout=ExperimentParameters.TIMEOUT)
    process.terminate()


@pytest.mark.parametrize("parameters", ExperimentParameters.PARAMETERS)
def test_graphs(parameters):
    columns = [3, 2]
    _, axes = pyplot.subplots(1, 2)
    for i, column in enumerate(columns):
        for j, machine in enumerate(Config.MACHINES):
            file = open(
                Config.LOGS +
                machine[0] + 
                str(parameters[2][j]) +
                ".txt",
                "r")
            lines = file.readlines()
            x = []
            y = []
            for line in lines:
                split = line.split(Config.DELIMITER)
                x.append(float(split[1]))
                y.append(int(split[column]))
            file.close()
            axes[i].plot(x, y)
    name = parameters[0]
    pyplot.savefig(Config.FIGURES + name + ".png")
    pyplot.close()
