"""Print 103 in a loop."""
from src.SProgram import SProgram as program


def main():
    """Print 101 in loop."""
    # program
    p = program(
        [["list1", 3]],
        fps=None,
        initialState="init",
        program=[
            ("init", [
                ["expr", ["$=", "list1[0]", "1"]],
                ["expr", ["$=", "list1[2]", "1"]],
                ["setState", "main"],
            ]),
            ("main", [
                # print "101"
                ["expr", ["$printInt", "list1[0]", "list1[0]"]],
                ["expr", ["$printInt", "0", "list1[1]"]],
                ["expr", ["$printInt_ln", "0", "list1[2]"]]
            ])
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
