"""Print 103 in a loop."""
from src.SProgram import SProgram as program
from src.conf.SStd import SStd


def main(argv=[], confs=[SStd()]):
    """Print 101 in loop."""
    # program
    p = program(
        [["list1", 3]],
        confs=confs,
        fps=None,
        initialState="init",
        states=[
            ("init", [
                ["expr", ["$=", "list1[0]", "1"]],
                ["expr", ["$=", "list1[2]", "1"]],
                ["expr", ["$=(const)=", "state", "@main"]],
            ]),
            ("main", [
                # print "101"
                ["expr", ["$printInt", "list1[0]"]],
                ["expr", ["$printInt", "list1[1]"]],
                ["expr", ["$printInt_ln", "list1[2]"]]
            ])
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
