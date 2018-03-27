"""Helper module for accessing functions."""
from src.SFunction import SFunction as sf
from src.SVariable import SVariable as sv


class SEsp8266:
    """Standard functions class for SScript."""
    def __init__(self, useVariables=True):
        self.useVariables = useVariables

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

    def getCpp(self, identifier):
        """Return c++ code related to this conf."""
        if identifier == "include":
            return ['#include "SEsp8266"']
        elif identifier == "functions_all":
            return ["SESP_FUNCTIONS_ALL"]
        return []
