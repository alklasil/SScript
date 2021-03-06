"""Simple if-else / swicth-case test."""
from src.SProgram import SProgram as program
from src.conf.SStd import SStd


def get_programData():
    return {
        "confs": [
            SStd
        ],
        "variableNameValuePairs": [
            "i"
        ],
        "states": [
            ("main", [

                # synchronous execution
                [
                    # store state "case" into tmp
                    # execute tmp (=="case") as a state
                    "$=(const)=", "tmp", "@case",
                    "$executeState", "tmp",
                    # print i
                    "$printInt_ln", "i"
                ],

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
                ["$=", "?", "i"],
                # case 0: i++
                ["$if", "?", "0", [
                    "$+", "i", "1",
                    "$return"
                ]],
                # case 1: i++, i++
                ["$if", "?", "1", [
                    ["$+", "i", "1"]*2,
                    "$return"
                ]],
                # default
                [
                    "$=", "i", "0",
                ]
            ]),

        ]
    }


def main(argv=[], programData=get_programData()):
    # program
    p = program(**programData)
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
