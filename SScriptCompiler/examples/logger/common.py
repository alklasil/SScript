"""Common methods."""


def variables(data):
    """Get variables (int32_t)."""
    return [
        [   # multipliers for sensors
            (name, value)
            for name, value in data['multipliers'].items()
        ],
        [   # other json specific variables
            (name, value) if type(value) is not list else value
            for name, value in data['variables'].items()
        ]
    ]


def strings(data):
    """Get strings (String)."""
    return [
        [   # common
            ("log", ""),
            ("space", " ")
        ],
        [   # json specific strings
            (name, value)
            for name, value in data['strings'].items()
        ]
    ]
