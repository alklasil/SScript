def lower_s(data):
    return ("<t", [
        [
            # read MPU
            "$mpu_readSensor",

            # get sensor value
            "$mpu_get" + data['sensorIdentifier'], data['sensorIdentifier'], "multiplier",

            # [?] = sensor value > tUP
            "$=", "?", data['sensorIdentifier'], "$>", "?", "tUP",

            # if [?] state = "t>"
            "$if", "1", "?", [
                "$=(const)=", "state", "@>t"
            ],

        ],
        # ["$printInt_ln", sensorIdentifier]
    ])
