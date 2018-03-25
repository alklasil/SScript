"""Count steps.

Increase step count when ...

"""
from src.SProgram import SProgram as program
from src.conf.std import Std as Std
from src.conf.mpu9250 import Mpu9250 as Mpu9250


def main():
    """Count steps."""
    # program

    std = Std()
    mpu9250 = Mpu9250()

    p = program(
        # variables (count & thresholds)
        [
            ("listLen", len(mpu9250.getVariables(None))),
            ("AccelMultiplier", 10),
            ("GyroMultiplier", 10),
            ("MagnMultiplier", 10),
            ("TemperatureMultiplier", 1),
        ],
        [
            ("log_str", ""),
            ("space", " ")
        ],
        confs=[std, mpu9250],
        fps=60,
        program=[
            ("main", [
                # read mpu & get store values to respective variables
                # The program can be expressed as 1 expression,
                # as there are no conditionals of any sort
                #   (-> pefromance++, size--)
                ["expr", [
                    # store get sampling time
                    "$readTimer",
                    "$getTime", 'millis',
                    # sample
                    "$mpu_readSensor",
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

                    # clear log_str
                    "$clearString", "log_str",

                    # add sampling time to log_str
                    "$concatString_Int", "log_str", "millis",
                    "$concatString_String", "log_str", "space",

                    # sensor values -> val1 val2 val3 ... valn
                    "$concatString_Int_List",
                    "log_str",
                    mpu9250.lastVariable(),
                    mpu9250.firstVariable(),

                    # print string
                    "$printString_ln", "log_str"

                    # store on the sdcard
                ]],

                # TODO: store on sd-card

            ])
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
