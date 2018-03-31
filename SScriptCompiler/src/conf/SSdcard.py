"""Helper module for accessing functions."""
from src.SFunction import SFunction
from src.SVariable import SVariable


class SSdcard:
    """Standard functions class for SScript."""
    def __init__(self, useVariables=True):
        self.useVariables = useVariables

    def getFunctions(self):
        """"Return a list of functions."""
        return [
            # basic operations
            SFunction("sdcard_open"),
            SFunction("sdcard_reopen"),
            SFunction("sdcard_write"),
            SFunction("sdcard_readString"),
            SFunction("sdcard_close"),
        ]

    def getVariables(self, sdict):
        """Return list of variables."""
        return []

    def getCpp(self, identifier):
        """Return c++ code related to this conf."""
        if identifier == "include":
            return ["#include <SSdcard.h>"]
        elif identifier == "functions_all":
            return ["SSDCARD_FUNCTIONS_ALL"]
        return []
