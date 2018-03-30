"""Print 123 in a loop with manual timers."""
from src.SProgram import SProgram as program
from src.conf.SStd import SStd


def main(argv=[], confs=[SStd()]):
    """Print 123 in loop."""
    # program
    p = program(
        # variables ["var1", ("var2", value), "var3", ("var4", value)]
        ["lastTimedOut", ("timeout_length", 1000), ("i", 123)],
        # set fps to manual
        confs=confs,
        fps=None,
        # program (state, [expressions])
        states=[
            ("main", [
                # read timer
                ["expr", ["$readTimer"]],

                # check if timeout_length since last tested
                # if not, return, otherwise, set lastTimedOut = millis

                ["expr", ["$timeout", "lastTimedOut", "timeout_length"]],
                # print
                ["expr", ["$printInt_ln", "i"]],
            ])
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
