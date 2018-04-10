def requestStringGenerator_s():
    return ("requestStringGeneratorState", [
        [
            # time
            "$readTimer",
            "$getTime", "millis",
            # timeOffset
            [
                # as int
                "$=", "timeOffset_millis", "millis",
                "$-", "timeOffset_millis", "sample_millis",
                # as string
                "$clearString", "#timeOffset_millis",
                "$concatString_Int", "#timeOffset_millis", "timeOffset_millis",
            ],
            # set esp requestString
            "$esp_setRequestStringHTMLWithTime", [
                "#requestString", "#timeOffset_millis"
            ],
        ]
    ])
