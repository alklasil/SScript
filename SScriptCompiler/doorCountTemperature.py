"""Count how many times a door has been opened based on temperature.

Increase count when temperature drops below down threshold.

Example output:
    21 4 3 1 4 1 19 15 20 10 5 1 3 2 4 10 1 7 4 2 9 2 4 2 8 4 3 1 3 13 3 17 3
    23 5 0 17 4 20 5 9 4 0 11 2 9 3 4 2 8 3 3 18 3 0 3 2 18 24 7 4 2 9 4 4 2 8
    4 3 1 3 13 3 17 3 23 5 0 17 4 19 5 9 4 0 11 2 9 2 4 2 8
"""
from src.SProgram import SProgram as program


def main():
    """Count how many times a door has been opened based on temperature."""
    # program
    p = program(
        # variables (count & thresholds)
        ["count", ("tUP", 15), ("tDOWN", 10)],
        # program (state, [expressions])
        initialState="init",
        program=[
            ("main", [
                ["executeState"]
            ]),
            ("init", [
                ["setState", ">t"]
            ]),
            (">t", [
                # read MPU
                ["readMPU"],

                # get temperature
                ["getMpuValue", "Temperature_C"],

                # [?] = temperature < tDOWN
                ["setConditional", "Temperature_C",  "<", "tDOWN"],

                # if [?] state = "<t>" for processing
                ["conditionalSetState", "<t>"]
            ]),
            ("<t>", [
                # state = "opening the door",
                #   (do not execute when closing the door)
                # increase count by one
                ["inc", "count"],
                # "debug" print the increased value
                ["printInt", "count"],
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
                ["conditionalSetState", ">t"]
            ]),
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
