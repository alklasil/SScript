"""Helper module for accessing functions."""
from src.SFunction import SFunction as sf
from src.SVariable import SVariable as sv

# TODO: divide this into smaller confs (smath, sstring, etc..)


class SStd:
    """Standard functions class for SScript."""
    def __init__(self, useVariables=True):
        self.useVariables = useVariables

    def getFunctions(self):
        """"Return a list of functions."""
        return [
            # basic operations
            sf("+"),                # leftValue += righValue
            sf("-"),
            sf("*"),                # leftValue /= rightValue
            sf("/"),
            sf("="),                # leftValue = rightValue
            sf("=(const)="),       # leftValue = const(rightValue),
                                    # do not parse rightValue
            sf("<"),                # leftValue < rightValue
            sf(">"),                # leftValue > rightValue
            sf("=="),               # leftValue == rightValue
            sf("!="),               # leftValue != rightValue
            # helper functions
            sf("executeState"),
            sf("if"),
            sf(";"),                # abort expression execution,
            sf("return"),           # abort state execution
                                    # leftvalue does not change
            # timer
            sf("readTimer"),
            sf("getTime"),
            sf("timeout"),

            # print (only int32_t for now)
            sf("printInt"),
            sf("printInt_ln"),
            sf("printString"),
            sf("printString_ln"),
            sf("clearString"),
            sf("concatString_String"),
            sf("concatString_Int"),
            sf("concatString_Int_List"),
        ]

    def getVariables(self, sdict):
        """Return list of variables."""
        if not self.useVariables:
            return []

        return [
            # basic variables
            sv("tmp"),
            sv("?"),
            sv("0"),
            sv("1", 1),
            sv("state", sdict["st"].get(sdict["initialState"])),

            # timer
            sv("millis"),
        ]

    def getCpp(self, identifier):
        """Return c++ code related to this conf."""
        if identifier == "include":
            return ["#include <SStd.h>"]
        elif identifier == "functions_all":
            return ["SSTD_FUNCTIONS_ALL"]
        return []
