"""Print in a loop."""
from src.SProgram import SProgram as program


def main():
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
            ("helloworld_str", "Hello world! "),
        ],
        # set frames/second = None == no fps limiter
        # (used for testing)
        #   (How to set fps for invidual states: See timerTest)
        #   (i.e., simple multithreading)
        fps=None,
        # program (state, [expressions])
        program=[
            ("main", [
                # increase count by one
                ["inc", "count"],
                # print("Hello world!", endl=False)
                ["printString", "helloworld_str"],
                # print(count, endl = True)
                ["printInt", "count", True],
            ])
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main()
