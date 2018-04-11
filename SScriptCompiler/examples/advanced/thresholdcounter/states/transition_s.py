def transition_s(data):
    return ("<t>", [
        [
            # increase count by one
            "$+", "count", "1",

            # Generate string: time count
            [
                # time
                "$getTime", "sample_millis",
                # clear (requestString)
                "$clearString", "#requestString",
                # concat configuration time
                "$concatString_Int", "#requestString", "configuration_millis",
                # space
                "$concatString_String", "#requestString", "#space",
                # concat current time
                "$concatString_Int", "#requestString", "sample_millis",
                # space
                "$concatString_String", "#requestString", "#space",
                # count integer
                "$concatString_Int", "#requestString", "count",
                # print
                "$printString_ln", "#requestString",
            ],
            # Write the string in sd-card
            [
                # open sd-card file for logging
                "$sdcard_open", [
                    "#logFile"
                ],
                "$sdcard_write", [
                    "#requestString"
                ],
                "$sdcard_close"
            ],

            # set state
            "$=(const)=", "state", "@<t"
        ],
    ])
