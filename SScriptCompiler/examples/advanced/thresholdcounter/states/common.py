"""Common methods."""


def getVariables(tUP, tDOWN, multiplier):
    return [
        "count",
        ("tUP", tUP),
        ("tDOWN", tDOWN),
        ("multiplier", multiplier),
        "configuration_millis",
        "sample_millis",
        "timeOffset_millis"
    ]


def getStrings(logFile):
    return [
        ("space", " "),
        ("requestString", ""),
        ("logFile", logFile),
        ("timeOffset_millis", "")
    ]


def parseCommandline(argv=[]):
    data = {}

    # TODO: better commandline argument parser
    data['tUP'] = int(argv[0])
    data['tDOWN'] = int(argv[1])
    data['sensorIdentifier'] = argv[2]
    data['multiplier'] = int(argv[3])
    # set filename (logFile) for example to current time in milliseconds (millis)
    #     This way you will be able to easily approximate the timings of events
    data['logFile'] = argv[4]

    return data


def programData(data):
    return {
        'variableNameValuePairs':
            getVariables(data['tUP'], data['tDOWN'], data['multiplier']),
        'stringNameValuePairs':
            getStrings(data['logFile']),
        'confs':
            data['confs'],
        'fps':
            60,
        'initialState':
            'init'
    }
