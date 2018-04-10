def upper_s(sensorIdentifier):
    return (">t", [
        [
            # read MPU
            "$mpu_readSensor",

            # get sensor value
            "$mpu_get" + sensorIdentifier, sensorIdentifier, "multiplier",

            # [?] = sensor value < tDOWN
            "$=", "?", sensorIdentifier, "$<", "?", "tDOWN",

            # if [?] state = "<t>" for processing
            "$if", "1", "?", [
                "$=(const)=", "state", "@<t>"
            ],
        ],
        #["$printInt_ln", sensorIdentifier],
    ])
