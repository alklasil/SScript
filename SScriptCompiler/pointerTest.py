"""Print 123555 in a loop using pointers."""
from src.SProgram import SProgram as program


def main():
    """Print 123555 in loop using pointers."""
    # program
    p = program(
        # variables ["var1", ("var2", value), "var3", ("var4", value)]
        [("i", 123), ("*i", "i"), ("j", 555), ("*j", "j")],
        # program (state, [expressions])
        program=[
            ("main", [
                # variables with name "*" + "anything" are pointers
                #   *i is a pointer to i, *j is a pointer to j
                #   pointers can be used the same way
                #   normal variables can be used.

                # print "123"
                ["printInt", "*i"],
                # print "555"
                ["printInt", "*j"]
            ])
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
