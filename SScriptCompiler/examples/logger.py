"""Count steps.

Increase step count when ...

"""
from src.SProgram import SProgram as program
from src.conf.SStd import SStd
from src.conf.SMpu9250 import SMpu9250


def get_programData():
    return {
        "confs": [
            SStd,
            SMpu9250
        ],
        "variableNameValuePairs": [
            ("listLen", len(SMpu9250().getVariables(None))),
            [   # multipliers for sensors
                ("AccelMultiplier", 10),
                ("GyroMultiplier", 10),
                ("MagnMultiplier", 10),
                ("TemperatureMultiplier", 1),
            ]
        ],
        "stringNameValuePairs": [
            ("log", ""),
            ("space", " ")
        ],
        "fps": 2,
        "states": [
            ("main", [
                # read mpu & get store values to respective variables
                # The program can be expressed as 1 expression,
                # as there are no conditionals of any sort
                #   (-> pefromance++, size--)
                [
                    # store get sampling time
                    "$readTimer",
                    "$getTime", 'millis',
                    # sample
                    "$mpu_readSensor", [
                        # Accel
                        "$mpu_getAccelX_mss", "AccelX_mss", "AccelMultiplier",
                        "$mpu_getAccelY_mss", "AccelY_mss", "AccelMultiplier",
                        "$mpu_getAccelZ_mss", "AccelZ_mss", "AccelMultiplier",
                        # Gyro
                        "$mpu_getGyroX_rads", "GyroX_rads", "GyroMultiplier",
                        "$mpu_getGyroY_rads", "GyroY_rads", "GyroMultiplier",
                        "$mpu_getGyroZ_rads", "GyroZ_rads", "GyroMultiplier",
                        # Magn
                        "$mpu_getMagX_uT", "MagX_uT", "MagnMultiplier",
                        "$mpu_getMagY_uT", "MagY_uT", "MagnMultiplier",
                        "$mpu_getMagZ_uT", "MagZ_uT", "MagnMultiplier",
                        # Temperature
                        "$mpu_getTemperature_C", "Temperature_C", "TemperatureMultiplier",
                    ],
                    # clear log_str
                    "$clearString", "#log",

                    # add sampling time to log_str
                    "$concatString_Int", "#log", "millis",
                    "$concatString_String", "#log", "#space",

                    # sensor values -> val1 val2 val3 ... valn
                    "$concatString_Int_List", [
                        "#log",                     # store in log
                        SMpu9250().lastVariable(),     # to (last element)
                        SMpu9250().firstVariable(),    # from (first element)
                    ],
                    # print string
                    "$printString_ln", "#log"

                    # store on the sdcard
                ],

                # TODO: store on sd-card

            ])
        ]
    }


def main(argv=[], programData=get_programData()):
    # program
    p = program(**programData)
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
