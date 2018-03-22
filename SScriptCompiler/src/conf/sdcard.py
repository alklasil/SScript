"""Helper module for accessing functions."""
from src.SFunction import SFunction as sf
from src.SVariable import SVariable as sv


class Std:
    """Standard functions class for SScript."""
    def __init__(self):
        """"""
        pass

    def getFunctions(self):
        """"Return a list of functions."""
        return [
            # basic operations
            sf("sdcard_open"),
            sf("sdcard_reopen"),
            sf("sdcard_write"),
            sf("sdcard_readString"),
            sf("sdcard_close"),
        ]

    def getVariables(self, sdict):
        """Return list of variables."""
        return []
