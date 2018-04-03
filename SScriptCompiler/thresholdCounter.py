"""Increase count when value below threshold from above threshold.
# TODO: better args comments
args:
    tUP = threshold up
    tDOWN = threshold down
    sensorIdentifier = see src.conf.mpu9255 variables (all but amplitudes)
        e.g. sensorIdentifier = "Temperature_C"
    multiplier -> sensorValue *= multiplier when measurement
example:
    python3 thresholdCounter.py 2 -2 GyroZ_rads 10 log.txt
# TODO: better filter function possibilities
# TODO(FIX): why does this return Wed Apr 04 2018 00:44:33 GMT+0300 (EEST): ;
        it should return Wed Apr 04 2018 00:44:33 GMT+0300 (EEST): x y z; where x, y, z are int32_t
    * (either SScript or ESP propably not working exactly right)
    * HOTFIX: either do not care, or use the version from history that worked
      (before esp_setRequestStringHTMLWithTime)
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
    sensorIdentifier = argv[2]
    multiplier = int(argv[3])
    # set filename (logFile) for example to current time in milliseconds (millis)
    #     This way you will be able to easily approximate the timings of events
    logFile = argv[4]

    # program
    p = program(
        # variables (count & thresholds)
        [
            "count",
            ("tUP", tUP),
            ("tDOWN", tDOWN),
            ("multiplier", multiplier),
            "configuration_millis",
            "sample_millis",
            "timeOffset_millis"
        ],
        [
            ("space", " "),
            ("requestString", ""),
            ("logFile", logFile),
            ("timeOffset_millis", "")
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
                    # set configuration time
                    "$getTime", "configuration_millis",

                    # set door open (closing does not add count)
                    "$=(const)=", "state", "@<t",
                    "$printInt_ln", sensorIdentifier,

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
                    "$mpu_get" + sensorIdentifier, sensorIdentifier, "multiplier",

                    # [?] = sensor value < tDOWN
                    "$=", "?", sensorIdentifier, "$<", "?", "tDOWN",

                    # if [?] state = "<t>" for processing
                    "$if", "1", "?", [
                        "$=(const)=", "state", "@<t>"
                    ],
                ],
                #["$printInt_ln", sensorIdentifier],
            ]),
            ("<t>", [
                # state = "opening the door",
                #   (do not execute when closing the door)
                [
                    # increase count by one
                    "$+", "count", "1",

                    # Generate string: time count
                    [
                        # time
                        "$getTime", "sample_millis",
                        # clear (requestString)
                        "$clearString", "#requestString",
                        # concat configuration time
                        "$concatString_Int", "#requestString", "configuration_millis",
                        # space
                        "$concatString_String", "#requestString", "#space",
                        # concat current time
                        "$concatString_Int", "#requestString", "sample_millis",
                        # space
                        "$concatString_String", "#requestString", "#space",
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
                    "$mpu_get" + sensorIdentifier, sensorIdentifier, "multiplier",

                    # [?] = sensor value < tDOWN
                    "$=", "?", sensorIdentifier, "$>", "?", "tUP",

                    # if [?] state = "<t>" for processing
                    "$if", "1", "?", [
                        "$=(const)=", "state", "@>t"
                    ],

                ],
                # ["$printInt_ln", sensorIdentifier]
            ]),
            ("requestStringGeneratorState", [
                [
                    # time
                    "$readTimer",
                    "$getTime", "millis",
                    # timeOffset
                    [
                        # as int
                        "$=", "timeOffset_millis", "millis",
                        "$-", "timeOffset_millis", "sample_millis",
                        # as string
                        "$clearString", "#timeOffset_millis",
                        # concat configuration time
                        "$concatString_Int", "#timeOffset_millis", "timeOffset_millis",
                    ],
                    # set esp requestString
                    "$esp_setRequestStringHTMLWithTime", [
                        "#requestString", "#timeOffset_millis"
                    ]
                ]
            ]),
        ])
    # compile and print the program
    p.compile()

if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv[1:])
