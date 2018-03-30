"""Increase count when value below threshold from above threshold.


# TODO: better args comments
args:
    tUP = threshold up
    tDOWN = threshold down
    sensorString = see src.conf.mpu9255 variables (all but amplitudes)
        e.g. sensorString = "Temperature_C"
    multiplier -> sensorValue *= multiplier when measurement

example:
    python3 thresholdCounter.py 2 -2 GyroZ_rads 10

# TODO: better filter function possibilities
"""

import sys
# import getopt

from src.SProgram import SProgram as program
from src.conf.SStd import SStd
from src.conf.SMpu9250 import SMpu9250


def main(argv=[], confs=[SStd(), SMpu9250()]):
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
            ("count", "count: ")
        ],
        confs=confs,
        fps=60,
        # program (state, [expressions])
        initialState="init",
        states=[
            ("init", [
                # TODO: add sensor-configuring here
                #   (Otherwise whis state is not required)

                # set door open (closing does not add count)
                [
                    "$=(const)=", "state", "@<t",
                    "$printInt_ln", sensorString
                ]

            ]),
            (">t", [
                [
                    # read MPU
                    "$mpu_readSensor",

                    # get sensor value
                    "$mpu_get" + sensorString, sensorString, "multiplier",

                    # [?] = sensor value < tDOWN
                    "$=", "?", sensorString, "$<", "?", "tDOWN",

                    # if [?] state = "<t>" for processing
                    "$if", "1", "?", "$=(const)=", "state", "@<t>",
                ]
                #["$printInt_ln", sensorString],
            ]),
            ("<t>", [
                # state = "opening the door",
                #   (do not execute when closing the door)
                [
                    # increase count by one
                    "$+", "count", "1",
                    # "debug" print the increased value
                    "$printString", "#count",
                    "$printInt_ln", "count",
                    # set state
                    "$=(const)=", "state", "@<t"
                ],
            ]),
            ("<t", [
                [
                    # read MPU
                    "$mpu_readSensor",

                    # get sensor value
                    "$mpu_get" + sensorString, sensorString, "multiplier",

                    # [?] = sensor value < tDOWN
                    "$=", "?", sensorString, "$>", "?", "tUP",

                    # if [?] state = "<t>" for processing
                    "$if", "1", "?", "$=(const)=", "state", "@>t",

                ],
                # ["$printInt_ln", sensorString]
            ]),
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv[1:])
