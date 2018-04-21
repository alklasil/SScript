def readSensor(sensorIdentifier):
    return ["$mpu_get" + sensorIdentifier, [
        sensorIdentifier,
        "multiplier",
    ]]


def readSensors(data):
    if data['sensorFunction'] == "":
        return readSensor(data['sensorIdentifier'])
    else:
        sensorIdentifier = data['sensorIdentifier'].split('_')
        begin = sensorIdentifier[0]
        end = sensorIdentifier[1]
        res = []
        # read sensors
        for xyz in ['X', 'Y', 'Z']:
            print(begin + xyz + "_" + end)
            res += readSensor(begin + xyz + "_" + end)
        # apply sensorFunction
        res += [data['sensorFunction'], [
            data['sensorIdentifier']
        ]]

        # res += ["$printInt_ln", data['sensorIdentifier']],

        return res


def compareSensors(data, operator, threshold):
    return [
        # [?] = sensor value > tUP
        "$=", "?", data['sensorIdentifier'], operator, "?", threshold,
    ]
