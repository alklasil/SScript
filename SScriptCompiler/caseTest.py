"""Simple if-else / swicth-case test."""
from src.SProgram import SProgram as program


def main():
    """Print 0 1 3 0...."""
    # program
    p = program(
        ["i"],
        # program (state, [expressions])
        program=[
            ("main", [
                # print i
                ["printInt", "i", True],

                # synchronous execution
                # store state "case" into tmp
                ["setState", "case", "tmp"],
                # execute tmp (=="case") as a state
                ["executeState", "tmp"],

                # asynchronous execution
                # This will be executed in the next loop
                #  (unless the state changes before that)
                # ["setState", "case"],
                # HOX! return state can be stored into a variable
                # in which case:
                #   state::main:
                #     # store the return ('address')
                #     ["setState", "main", "nextState"],
                #     # set state
                #     ["setState", "case"],
                #   state::case
                #     # nextState is a variable, use 'set' to set state
                #     ["set", "state", "nextState"],
            ]),
            ("case", [
                # switch(i) {
                # (This is not necessary, you can use i directly in the sates,
                #  but if the switch(equation) were more complex it is
                #  recommended to do this way)
                ["expr", ["=", "?", "i"]],
                    # case 0: i++
                    ["expr", ["if", "?", "0", "+", "i", "1", "return"]],
                    # case 1: i++, i++ (just for test, faster ways exist)
                    ["expr", ["if", "?", "1", "+", "i", "1", "+", "i", "1", "return"]],
                    # default (i != 0 && i != 1, e.g., i == 3)
                    ["expr", ["=", "i", "0"]],
                # }

                # if asynchronous execution
                # go back to the main state in the next loop
                # #["setState", "main"],
            ]),

        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
