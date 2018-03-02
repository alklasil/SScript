"""Print 103 in a loop."""
from src.SProgram import SProgram as program


def main():
    """Print 103 in loop."""
    # program
    p = program(
        # variables ["var1", ("var2", value), "var3",
        # ("var4", value), ["list1", size]]
        [["list1", 3]],
        # program (state, [expressions])
        initialState="init",
        program=[
            ("init", [
                ["set", "list1[0]", 1],
                # ["list1[1]", 0], variables initialize to 0
                ["set", "list1[2]", 3],
                ["setState", "main"],
            ]),
            ("main", [
                # print "103"
                ["printInt", "list1[0]"],
                ["printInt", "list1[1]"],
                ["printInt", "list1[2]"]
            ])
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
