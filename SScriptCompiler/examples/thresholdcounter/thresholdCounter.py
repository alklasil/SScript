"""Increase count when value goes below threshold from above threshold."""
# 'std'
import sys
import json

# SScript
from src.SProgram import SProgram as program

# SScript confs
from src.conf.SStd import SStd
from src.conf.SMpu9250 import SMpu9250
from src.conf.SEsp8266 import SEsp8266
from src.conf.SSdcard import SSdcard

# states
from .states.init_s import init_s
from .states.upper_s import upper_s
from .states.transition_s import transition_s
from .states.lower_s import lower_s
from .states.requestStringGenerator_s import requestStringGenerator_s

# common
from .common import variables
from .common import strings


argv = sys.argv[1:]


def get_programData(argv=argv):

    # check if json file provided
    if len(argv) is not 1:
        print("usage: python3 -m examples.thresholdcounter.thresholdCounter 'examples/thresholdcounter/json/<file.json>'")
        print("example: python3 -m examples.thresholdcounter.thresholdCounter 'examples/thresholdcounter/json/stepcounter.json'")
        sys.exit(2)

    # if json file provided, load it into data as dict
    data = json.load(open(argv[0]))

    return {
        "confs": [
            SStd,
            SMpu9250,
            SEsp8266,
            SSdcard
        ],
        "variableNameValuePairs": [
            variables(data)
        ],
        "stringNameValuePairs": [
            strings(data)
        ],
        "fps":
            data['fps'],
        "initialState":
            data['initialState'],
        "states": [
            # init state (set values & handles)
            [
                init_s(data),   # init
            ],
            # main states (measure & process & store)
            [
                upper_s(data),          # value above upper threshold state
                transition_s(data),     # transition from upper to lower state
                lower_s(data),          # value below lower threshold state
            ],
            # other (calls from c++)
            [
                requestStringGenerator_s(data),     # generate requestString
            ]
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
