def init_s(sensorIdentifier):
    return ("init", [
        [
            # set configuration time
            "$getTime", "configuration_millis",

            # set state initially below lower threshold
            "$=(const)=", "state", "@<t",
            "$printInt_ln", sensorIdentifier,

            # set requestStringGenerator
            "$esp_setRequestStringGenerator", [
                "@requestStringGeneratorState"
            ],
        ],
    ])
