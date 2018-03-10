"""Count how many times a door has been opened based on temperature.

Increase count when temperature drops below down threshold.

Example output:
    21 4 3 1 4 1 19 15 20 10 5 1 3 2 4 10 1 7 4 2 9 2 4 2 8 4 3 1 3 13 3 17 3
    23 5 0 17 4 20 5 9 4 0 11 2 9 3 4 2 8 3 3 18 3 0 3 2 18 24 7 4 2 9 4 4 2 8
    4 3 1 3 13 3 17 3 23 5 0 17 4 19 5 9 4 0 11 2 9 2 4 2 8
"""
from src.SProgram import SProgram as program
from src.conf.std import Std as Std
from src.conf.mpu9250 import Mpu9250 as Mpu9250

def main():
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
        confs=[Std(), Mpu9250()],
        fps=100,
        # program (state, [expressions])
        initialState="init",
        program=[
            ("init", [
                # TODO: add sensor-configuring here
                #   (Otherwise whis state is not required)

                # set door open (closing does not add count)
                ["setState", "<t"],
                ["printInt", "Temperature_C"]
            ]),
            (">t", [
                # read MPU
                ["readMPU"],

                # get temperature
                ["getMpuValue", "Temperature_C"],

                # [?] = temperature < tDOWN
                ["setConditional", "Temperature_C",  "<", "tDOWN"],

                # if [?] state = "<t>" for processing
                ["conditionalSetState", "<t>"],

                #["printInt", "Temperature_C", True]
            ]),
            ("<t>", [
                # state = "opening the door",
                #   (do not execute when closing the door)
                # increase count by one
                ["inc", "count"],
                # "debug" print the increased value
                ["printString", "count_str"],
                ["printInt", "count", True],
                # set state
                ["setState", "<t"]
            ]),
            ("<t", [
                # read mpu sensor
                ["readMPU"],

                # get temperature
                ["getMpuValue", "Temperature_C"],

                # [?] = temperature > tDOWN
                ["setConditional", "Temperature_C", ">", "tUP"],

                # if [?] state = "<t"
                ["conditionalSetState", ">t"],

                #["printInt", "Temperature_C", True]
            ]),
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
