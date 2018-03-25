"""Helper module for accessing functions."""
from src.SFunction import SFunction as sf
from src.SVariable import SVariable as sv


class Esp8266:
    """Standard functions class for SScript."""
    def __init__(self):
        """"""
        pass

    def getFunctions(self):
        """"Return a list of functions."""
        return [
            # basic operations
            sf("esp_setRequestString"),
            sf("esp_setRequestStringGenerator")
        ]

    def getVariables(self, sdict):
        """Return list of variables."""
        return []
