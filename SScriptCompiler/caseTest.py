"""Simple if-else / swicth-case test."""
from src.SProgram import SProgram as program
from src.conf.SStd import SStd


def main(argv=[], confs=[SStd()]):
    """Print 0 1 3 0...."""
    # program
    p = program(
        ["i"],
        confs=confs,
        # program (state, [expressions])
        program=[
            ("main", [

                # synchronous execution
                ["expr", [
                    # store state "case" into tmp
                    "$=(const)=", "tmp", "@case",
                    # execute tmp (=="case") as a state
                    "$executeState", "tmp",
                    # print i
                    "$printInt_ln", "i"
                ]],

                # The switch-case statement (state) can also be executed asynchronously:
                # (i.e., execute in the next loop.)
                # (may be good option if switch-case statement is more complex)
                # (There are multiple ways of executing the switch-case statement
                #  asynchronously: below is one of them)
                #   Set state=proxy, set proxyState=case, set returnState=main
                #      (nextLoop) state::proxy::executeState(proxyState)
                #      (nextLoop) state::proxy::set state=returnState
            ]),
            ("case", [
                # switch(i) {
                # (This is not necessary, you can use i directly in the sates,
                #  but if the switch(equation) were more complex it is
                #  recommended to do this way)
                ["expr", ["$=", "?", "i"]],
                #   case 0: i++
                    ["expr", ["$if", "?", "0", "$+", "i", "1", "$return"]],
                #   case 1: i++, i++ (just for test, faster ways exist)
                    ["expr", ["$if", "?", "1", "$+", "i", "1", "$+", "i", "1", "$return"]],
                #   default (i != 0 && i != 1, e.g., i == 3)
                    ["expr", ["$=", "i", "0"]],
                # }
            ]),

        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
