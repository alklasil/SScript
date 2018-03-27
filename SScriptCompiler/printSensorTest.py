"""Print in a loop."""
from src.SProgram import SProgram as program
from src.conf.SStd import SStd
from src.conf.SMpu9250 import SMpu9250


def main(argv=[], confs=[SStd(), SMpu9250()]):
    """Print 'Hello world!' and similar texts in loop."""
    # program
    p = program(
        confs=[SStd(), SMpu9250()],
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
