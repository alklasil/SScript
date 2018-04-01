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
from src.conf.SEsp8266 import SEsp8266
from src.conf.SSdcard import SSdcard


def main(argv=[], confs=[SStd(), SMpu9250(), SEsp8266(), SSdcard()]):
    """Increase count based on thresholding."""
    # TODO: better commandline argument parser
    tUP = int(argv[0])
    tDOWN = int(argv[1])
    sensorString = argv[2]
    multiplier = int(argv[3])
    logFile = argv[4]

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
            ("count", " count: "),
            ("requestString", ""),
            ("logFile", logFile)
        ],
        confs=confs,
        fps=60,
        # program (state, [expressions])
        initialState="init",
        states=[
            ("init", [
                # TODO: add sensor-configuring here
                #   (Otherwise whis state is not required)

                [
                    # set door open (closing does not add count)
                    "$=(const)=", "state", "@<t",
                    "$printInt_ln", sensorString,

                    # set requestStringGenerator
                    "$esp_setRequestStringGenerator", [
                        "@requestStringGeneratorState"
                    ],
                ],
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
                    "$if", "1", "?", [
                        "$=(const)=", "state", "@<t>"
                    ],
                ],
                #["$printInt_ln", sensorString],
            ]),
            ("<t>", [
                # state = "opening the door",
                #   (do not execute when closing the door)
                [
                    # increase count by one
                    "$+", "count", "1",

                    # Generate string: time #count: count
                    [
                        # clear
                        "$clearString", "#requestString",
                        # time
                        "$getTime", "millis",
                        "$concatString_Int", "#requestString", "millis",
                        # count string
                        "$concatString_String", "#requestString", "#count",
                        # count integer
                        "$concatString_Int", "#requestString", "count",
                        # print
                        "$printString_ln", "#requestString",
                    ],
                    # Write the string in sd-card
                    [
                        # open sd-card file for logging
                        "$sdcard_open", [
                            "#logFile"
                        ],
                        "$sdcard_write", [
                            "#requestString"
                        ],
                        "$sdcard_close"
                    ],

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
                    "$if", "1", "?", [
                        "$=(const)=", "state", "@>t"
                    ],

                ],
                # ["$printInt_ln", sensorString]
            ]),
            ("requestStringGeneratorState", [
                [
                    # format requestString
                    "$printString_ln", "#requestString",
                    # set esp requestString
                    "$esp_setRequestString", [
                        "#requestString",
                    ]
                ]
            ]),
        ])
    # compile and print the program
    p.compile()

if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv[1:])
