"""Print in a loop."""
from src.SProgram import SProgram as program
from src.conf.SStd import SStd


def main(argv=[], confs=[SStd()]):
    print(confs)
    """Print 'Hello world!' int(count) in a loop."""
    # program
    p = program(
        variableNameValuePairs=[
            # initialize count = 0
            "count"
            # initialize count = 1
            # ("count", 1)
            # create list("count", 3) (= count[0], count[1], count[2])
            # ["count", 3]
        ],
        # set strings
        stringNameValuePairs=[
            ("helloworld", "Hello world! "),
        ],
        # set frames/second = None == no fps limiter
        # (used for testing)
        #   (How to set fps for invidual states: See timerTest)
        #   (i.e., simple multithreading)
        confs=confs,
        fps=60,
        # program (state, [expressions])
        states=[
            ("main", [
                [
                    # increase count by one
                    "$+", "count", "1",
                    # print("Hello world!", endl=False)
                    "$printString_ln", "#helloworld",
                    # print(count, endl = True)
                    "$printInt_ln", "count"
                ],
            ])
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
