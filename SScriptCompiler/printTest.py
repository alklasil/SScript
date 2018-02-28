"""Print 123 in a loop."""
from src.SProgram import SProgram as program


def main():
    """Print 123 in loop."""
    # program
    p = program(
        # variables ["var1", ("var2", value), "var3", ("var4", value)]
        [("i", 123)],
        # program (state, [expressions])
        program=[
            ("main", [
                ["printInt", "i"]
            ])
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
