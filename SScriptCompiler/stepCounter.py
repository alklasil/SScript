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
        fps=100,
        program=[
            ("main", [
                # read MPU
                ["expr", ["$mpu_readSensor"]],

                # How do we count the steps
                #   (1) frequency? (FFT + MAX amplitude + timeout)
                #   (2) derivative? dAmplitude > tUP -> count++
                #   (3) integral / mean / max / threshold?
                #          > tUp -> count
                #  matlab the data first

            ])
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
