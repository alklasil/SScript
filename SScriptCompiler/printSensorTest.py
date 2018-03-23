"""Print in a loop."""
from src.SProgram import SProgram as program
from src.conf.std import Std as Std
from src.conf.mpu9250 import Mpu9250 as Mpu9250


def main():
    """Print 'Hello world!' and similar texts in loop."""
    # program
    p = program(
        confs=[Std(), Mpu9250()],
        fps=2,
        program=[
            ("main", [
                # read MPU
                ["expr", ["$mpu_readSensor"]],

                # get temperature
                ["expr", ["$mpu_getTemperature_C", "Temperature_C", "1"]],

                # print
                ["expr", ["$printInt_ln", "Temperature_C"]],

            ])
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
