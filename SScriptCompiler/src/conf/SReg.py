"""Helper module for accessing functions."""
from src.SVariable import SVariable as sv


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
            sv("r1"), sv("r2"),
            sv("r3"), sv("r4"),
            sv("r5"), sv("r6"),
            sv("r7"), sv("r8"),
        ]
        pass
