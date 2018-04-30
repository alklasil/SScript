def readSensors(data):
    return [
        "$mpu_readSensor", [

            data['getSensors']
        ]
    ]


def tilt(data):
    return [
        # roll (roll = atan2(y, z))
        [
            "$atan2", ["roll", "AccelY_mss", "AccelZ_mss"]
        ],
        # pitch (pitch = atan2(-x, sqrt(y*y + z*z)))
        [
            # "-x" = -AccelX_mss
            "$=", "-x", "0", "$-", "-x", "AccelX_mss",
            # y*y = AccelY_mss * AccelY_mss
            "$=", "y*y", "AccelY_mss", "$*", "y*y", "AccelY_mss",
            # z*z = AccelZ_mss * AccelZ_mss
            "$=", "z*z", "AccelZ_mss", "$*", "z*z", "AccelZ_mss",
            # y*y + z*z
            "$=", "y*y + z*z", "y*y", "$+", "y*y + z*z", "z*z",
            # sqrt(y*y + z*z) = sqrt(y*y + z*z)
            "$sqrt", ["sqrt(y*y + z*z)", "y*y + z*z"],
            # pitch =
            "$atan2", ["roll", "-x", "sqrt(y*y + z*z)"]
        ]
    ]


def processSensors(data):
    if 'processSensors' in data:
        func = globals()[data['processSensors']]
        return func(data)
    return []


def clearString(data):
    return [
        # clear log_str
        "$clearString", "#log",
    ]


def logTime(data):
    return [
        # add sampling time to log_str
        "$concatString_Int", "#log", "millis",
        "$concatString_String", "#log", "#space",
    ]


def logSensors(data):
    return [
        # sensor values -> val1 val2 val3 ... valn
        "$concatString_Int_List", [
            "#log",                       # store into log
            data['log']['to'],    # to (last sensor name)
            data['log']['from'],     # from (first sensor name)
        ]
    ]


def generateLogString(data):
    return [
        clearString(data),
        logTime(data),
        logSensors(data)
    ]


def printLogString(data):
    return [
        "$printString_ln", "#log"
    ]


def getTime(data):
    return [
        "$readTimer", [
            "$getTime", 'millis',
        ]
    ]
