"""Count how many times a door has been opened based on temperature.

Increase count when temperature drops below down threshold.

TODO: modify this to be configurable to use either temperature, accl or gyro
      (commandline parameters -> different output)
"""
from src.SProgram import SProgram as program
from src.conf.SStd import SStd
from src.conf.SMpu9250 import SMpu9250


def main(argv=[], confs=[SStd(), SMpu9250()]):
    """Count how many times a door has been opened based on temperature."""
    # program
    p = program(
        # variables (count & thresholds)
        [
            "count",
            ("tUP", 17),
            ("tDOWN", 12)
        ],
        [
            # HOX! there cannot be similarly named variables and strings
            # count and _count are equal,
            ("count_str", "count(door opened): ")
        ],
        confs=confs,
        fps=100,
        # program (state, [expressions])
        initialState="init",
        program=[
            ("init", [
                # TODO: add sensor-configuring here
                #   (Otherwise whis state is not required)

                # set door open (closing does not add count)
                ["expr", ["$=(const)=", "state", "@<t"]],
                ["expr", ["$printInt_ln", "Temperature_C"]]

            ]),
            (">t", [
                # read MPU
                ["expr", ["$mpu_readSensor"]],

                # get temperature
                ["expr", ["$mpu_getTemperature_C", "Temperature_C", "1"]],

                # [?] = temperature < tDOWN
                ["expr", ["$=", "?", "Temperature_C", "$<", "?", "tDOWN"]],

                # if [?] state = "<t>" for processing
                ["expr", ["$if", "0", "?", "$=(const)=", "state", "@<t>"]],

                ["expr", ["$printInt_ln", "Temperature_C"]],
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

                # get temperature
                ["expr", ["$mpu_getTemperature_C", "Temperature_C", "1"]],

                # [?] = temperature < tDOWN
                ["expr", ["$=", "?", "Temperature_C", "$>", "?", "tUP"]],

                # if [?] state = "<t>" for processing
                ["expr", ["$if", "0", "?", "$=(const)=", "state", "@>t"]],

                ["expr", ["$printInt_ln", "Temperature_C"]],
            ]),
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
