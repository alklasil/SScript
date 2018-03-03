"""Print in a loop using pointers."""
from src.SProgram import SProgram as program


def main():
    """Print in a loop using pointers."""
    # program
    p = program(
        # variables ["var1", ("var2", value), "var3", ("var4", value)]
        [("i", "b"), ("a", 333), ("b", 555)],
        # program (state, [expressions])
        program=[
            ("main", [
                # use i to as 'pointer' for b
                # *i -> variables[i.value].value

                # print 555
                ["printInt", "*i"],
            ])
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
