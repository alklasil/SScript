"""Common methods."""


def variables(data):
    """Get variables (int32_t)."""
    return [
        "count",
        ("tUP", data['tUP']),
        ("tDOWN", data['tDOWN']),
        ("multiplier", data['multiplier']),
        "configuration_millis",
        "sample_millis",
        "timeOffset_millis"
    ]


def strings(data):
    """Get strings (String)."""
    return [
        ("space", " "),
        ("requestString", ""),
        ("logFile", data['logFile']),
        ("timeOffset_millis", "")
    ]
