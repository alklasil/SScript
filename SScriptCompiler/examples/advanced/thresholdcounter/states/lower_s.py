def lower_s(sensorIdentifier):
    return ("<t", [
        [
            # read MPU
            "$mpu_readSensor",

            # get sensor value
            "$mpu_get" + sensorIdentifier, sensorIdentifier, "multiplier",

            # [?] = sensor value > tUP
            "$=", "?", sensorIdentifier, "$>", "?", "tUP",

            # if [?] state = "t>"
            "$if", "1", "?", [
                "$=(const)=", "state", "@>t"
            ],

        ],
        # ["$printInt_ln", sensorIdentifier]
    ])
