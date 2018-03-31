"""Helper module for accessing functions."""
from src.SVariable import SVariable


class SReg:
    """Standard functions class for SScript."""
    def __init__(self, useVariables=True):
        self.useVariables = useVariables

    def getFunctions(self):
        """"Return a list of functions."""
        return []

    def getVariables(self, sdict):
        """Return list of variables."""
        if not self.useVariables:
            return []

        return [
            # a few 'registers' for general use
            SVariable("r1"), SVariable("r2"),
            SVariable("r3"), SVariable("r4"),
            SVariable("r5"), SVariable("r6"),
            SVariable("r7"), SVariable("r8"),
        ]
        pass
