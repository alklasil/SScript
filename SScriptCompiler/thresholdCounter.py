"""Increase count when value below threshold from above threshold.


# TODO: better args comments
args:
    tUP = threshold up
    tDOWN = threshold down
    sensorString = see src.conf.mpu9255 variables (all but amplitudes)
        e.g. sensorString = "Temperature_C"
    multiplier -> sensorValue *= multiplier when measurement

example:
    python3 thresholdCounter.py 100 -100 GyroZ_rads 10

# TODO: better filter function possibilities
"""

import sys
# import getopt

from src.SProgram import SProgram as program
from src.conf.std import Std as Std
from src.conf.mpu9250 import Mpu9250 as Mpu9250


def main(argv):
    """Increase count based on thresholding."""
    # TODO: better commandline argument parser
    tUP = int(argv[0])
    tDOWN = int(argv[1])
    sensorString = argv[2]
    multiplier = int(argv[3])

    # program
    p = program(
        # variables (count & thresholds)
        [
            "count",
            ("tUP", tUP),
            ("tDOWN", tDOWN),
            ("multiplier", multiplier)
        ],
        [
            # HOX! there cannot be similarly named variables and strings
            # count and _count are equal,
            ("count_str", "count: ")
        ],
        confs=[Std(), Mpu9250()],
        fps=60,
        # program (state, [expressions])
        initialState="init",
        program=[
            ("init", [
                # TODO: add sensor-configuring here
                #   (Otherwise whis state is not required)

                # set door open (closing does not add count)
                ["expr", ["$=(const)=", "state", "@<t"]],
                ["expr", ["$printInt_ln", sensorString]]

            ]),
            (">t", [
                # read MPU
                ["expr", ["$mpu_readSensor"]],

                # get sensor value
                ["expr", ["$mpu_get" + sensorString, sensorString, "multiplier"]],

                # [?] = sensor value < tDOWN
                ["expr", ["$=", "?", sensorString, "$<", "?", "tUP"]],

                # if [?] state = "<t>" for processing
                ["expr", ["$if", "0", "?", "$=(const)=", "state", "@<t>"]],

                # ["expr", ["$printInt_ln", sensorString]],
            ]),
            ("<t>", [
                # state = "opening the door",
                #   (do not execute when closing the door)
                # increase count by one
                ["expr", ["$+", "count", "1"]],
                # "debug" print the increased value
                ["expr", ["$printString", "count_str"]],
                ["expr", ["$printInt_ln", "count"]],
                # set state
                ["expr", ["$=(const)=", "state", "@<t"]],
            ]),
            ("<t", [
                # read MPU
                ["expr", ["$mpu_readSensor"]],

                # get sensor value
                ["expr", ["$mpu_get" + sensorString, sensorString, "multiplier"]],

                # [?] = sensor value < tDOWN
                ["expr", ["$=", "?", sensorString, "$>", "?", "tDOWN"]],

                # if [?] state = "<t>" for processing
                ["expr", ["$if", "0", "?", "$=(const)=", "state", "@>t"]],

                # ["expr", ["$printInt_ln", sensorString]],
            ]),
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv[1:])
