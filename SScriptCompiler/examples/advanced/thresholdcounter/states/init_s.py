def init_s(data):
    return ("init", [
        [
            # set configuration time
            "$getTime", "configuration_millis",

            # set state initially below lower threshold
            "$=(const)=", "state", "@<t",
            "$printInt_ln", data['sensorIdentifier'],

            # set requestStringGenerator
            "$esp_setRequestStringGenerator", [
                "@requestStringGeneratorState"
            ],
        ],
    ])
