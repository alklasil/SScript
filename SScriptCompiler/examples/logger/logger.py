"""logger."""
# 'std'
import sys
import json


from src.SProgram import SProgram as program
from src.conf.SStd import SStd
from src.conf.SMpu9250 import SMpu9250


from .common import variables
from .common import strings
from .src.common import readSensors, generateLogString, getTime, printLogString, processSensors


argv = sys.argv[1:]


def get_programData(argv=argv):

    # check if json file provided
    if len(argv) is not 1:
        print("usage: python3 -m examples.logger.logger 'examples/logger/json/<file.json>'")
        print("example: python3 -m examples.logger.logger 'examples/logger/json/logger.json'")
        sys.exit(2)

    # if json file provided, load it into data as dict
    data = json.load(open(argv[0]))

    return {
        "confs": [
            SStd,
            SMpu9250
        ],
        "variableNameValuePairs": [
            variables(data)
        ],
        "stringNameValuePairs": [
            strings(data)
        ],
        "fps": data['fps'],
        "states": [
            ("main", [
                [
                    getTime(data),
                    readSensors(data),
                    processSensors(data),
                    generateLogString(data),
                    printLogString(data),
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
    main(argv)
