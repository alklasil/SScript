"""Print in a loop."""
from src.SProgram import SProgram as program


def main():
    """Print 'Hello world!' and similar texts in loop."""
    # program
    p = program(
        fps=2,
        program=[
            ("main", [
                # read MPU
                ["readMPU"],

                # get temperature
                ["getMpuValue", "Temperature_C"],

                # print
                ["printInt", "Temperature_C", True],

            ])
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
