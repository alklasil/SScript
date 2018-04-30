def readSensors(data):
    return [
        "$mpu_readSensor", [

            data['getSensors']
        ]
    ]


def tilt(data):
    return []


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
