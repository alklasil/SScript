from .common import readSensors
from .common import compareSensors


def upper_s(data):
    return (">t", [
        [
            # read MPU
            "$mpu_readSensor",

            # read sensors
            readSensors(data),

            # compare sensors. store result in '?'
            compareSensors(data),

            # if [?] state = "<t>" for processing
            "$if", "1", "?", [
                "$=(const)=", "state", "@<t>"
            ],
        ],
    ])
