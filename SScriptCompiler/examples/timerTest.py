"""Print 123 in a loop with manual timers."""
from src.SProgram import SProgram as program
from src.conf.SStd import SStd


def get_programData():
    return {
        "confs": [
            SStd
        ],
        "variableNameValuePairs": [
            "lastTimedOut",
            ("timeout_length", 1000),
            ("i", 123)
        ],
        "stringNameValuePairs": [
            ("helloworld", "Hello world! ")
        ],
        "fps": None,
        "states": [
            ("main", [
                # read timer
                [
                    "$readTimer",

                    # check if timeout_length since last tested
                    # if not: return,
                    # otherwise: set lastTimedOut = millis
                    "$timeout", "lastTimedOut", "timeout_length",

                    # print i & \n
                    "$printInt_ln", "i",
                ]
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
