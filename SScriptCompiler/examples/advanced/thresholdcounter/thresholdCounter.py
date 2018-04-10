"""Increase count when value below threshold from above threshold.
# TODO: better args comments
args:
    tUP = threshold up
    tDOWN = threshold down
    sensorIdentifier = see src.conf.mpu9255 variables (all but amplitudes)
        e.g. sensorIdentifier = "Temperature_C"
    multiplier -> sensorValue *= multiplier when measurement
example:
    stepcounter:
        python3 -m examples.advanced.thresholdCounter 2 -2 GyroZ_rads 10 log.txt
"""

# commandline arguments
import sys

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
from .common import parseCommandline
from .common import programData


def main(argv=[], confs=[SStd(), SMpu9250(), SEsp8266(), SSdcard()]):
    """Increase count based on thresholding."""
    # TODO: read variables, strings, etc from a json file/files
    #       stepCounter.json,
    #       doorCounter.json,
    #       etc,

    data = parseCommandline(argv)
    data['confs'] = confs

    # program
    p = program(
        # initialize variables (see common.py)
        **programData(data),
        # set states (see states/*)
        states=[
            # init (set values, handles, etc..)
            [
                init_s(data['sensorIdentifier']),
            ],
            # main (measure, process, store)
            [
                # value above upper threshold state
                upper_s(data['sensorIdentifier']),
                # transition state from above upper threshold to below lower threshold
                transition_s(),
                # value below lower threshold state
                lower_s(data['sensorIdentifier']),
            ],
            # handles (not called internally)
            [
                # generate requestString if esp receives get-request
                requestStringGenerator_s(),
            ]
        ])
    # compile and print the program
    p.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv[1:])
