def upper_s(data):
    return (">t", [
        [
            # read MPU
            "$mpu_readSensor",

            # get sensor value
            "$mpu_get" + data['sensorIdentifier'], data['sensorIdentifier'], "multiplier",

            # [?] = sensor value < tDOWN
            "$=", "?", data['sensorIdentifier'], "$<", "?", "tDOWN",

            # if [?] state = "<t>" for processing
            "$if", "1", "?", [
                "$=(const)=", "state", "@<t>"
            ],
        ],
        #["$printInt_ln", sensorIdentifier],
    ])
