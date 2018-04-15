"""Print in a loop."""
from src.SProgram import SProgram as program
from src.conf.SStd import SStd


def get_programData():
    return {
        "confs": [
            SStd
        ],
        "variableNameValuePairs": [
            "count"
        ],
        "stringNameValuePairs": [
            ("helloworld", "Hello world! ")
        ],
        "fps": 60,
        "states": [
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
