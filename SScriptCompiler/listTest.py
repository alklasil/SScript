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
                [
                    "$=", "list1[0]", "1",
                    "$=", "list1[2]", "1",
                    "$=(const)=", "state", "@main"
                ],
            ]),
            ("main", [
                # print "101"
                [
                    "$printInt", "list1[0]",
                    "$printInt", "list1[1]",
                    "$printInt_ln", "list1[2]"
                ]
            ])
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
