from .common import readSensors
from .common import compareSensors


def lower_s(data):
    return ("<t", [
        [
            # read MPU
            "$mpu_readSensor",

            # read sensors
            readSensors(data),

            # compare sensors. store result in '?'
            compareSensors(data, "$>", 'tUP'),

            # if [?] state = "t>"
            "$if", "1", "?", [
                "$=(const)=", "state", "@>t"
            ],

        ],
    ])
