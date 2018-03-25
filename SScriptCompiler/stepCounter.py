"""Count steps.

Increase step count when ...

"""
from src.SProgram import SProgram as program
from src.conf.std import Std as Std
from src.conf.mpu9250 import Mpu9250 as Mpu9250


def main():
    """Count steps."""
    # program
    p = program(
        # variables (count & thresholds)
        [
            "count"
        ],
        [
            ("count_str", "count(steps): ")
        ],
        confs=[Std(), Mpu9250()],
        fps=20,
        program=[
            ("main", [
                # read MPU
                ["expr", ["$mpu_readSensor"]],
                # get MagZ_uT
                ["expr", ["$mpu_getMagZ_uT", "MagZ_uT", "1"]],

            ])
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
