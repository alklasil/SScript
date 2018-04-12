"""Helper module for accessing functions."""
from src.SFunction import SFunction
from src.SVariable import SVariable
# TODO: divide this into smaller confs (smath, sstring, etc..)


class SStd:
    """Standard functions class for SScript."""
    def __init__(self, useVariables=True):
        self.useVariables = useVariables

    def getFunctions(self):
        """"Return a list of functions."""
        return [
            # basic operations
            SFunction("+"),                # leftValue += righValue
            SFunction("-"),
            SFunction("*"),                # leftValue /= rightValue
            SFunction("/"),
            SFunction("="),                # leftValue = rightValue
            SFunction("=(const)="),       # leftValue = const(rightValue),
                                    # do not parse rightValue
            SFunction("<"),                # leftValue < rightValue
            SFunction(">"),                # leftValue > rightValue
            SFunction("=="),               # leftValue == rightValue
            SFunction("!="),               # leftValue != rightValue
            SFunction("maxXYZ"),           # max(x, y, z)
            # helper functions
            SFunction("executeState"),
            SFunction("if"),
            SFunction(";"),                # abort expression execution,
            SFunction("return"),           # abort state execution
                                    # leftvalue does not change
            # timer
            SFunction("readTimer"),
            SFunction("getTime"),
            SFunction("timeout"),

            # print (only int32_t for now)
            SFunction("printInt"),
            SFunction("printInt_ln"),
            SFunction("printString"),
            SFunction("printString_ln"),
            SFunction("clearString"),
            SFunction("concatString_String"),
            SFunction("concatString_Int"),
            SFunction("concatString_Int_List"),
        ]

    def getVariables(self, sdict):
        """Return list of variables."""
        if not self.useVariables:
            return []

        stateNames = sdict["states"]
        initialState = stateNames.get(sdict["initialState"])

        return [
            # basic variables
            SVariable("tmp"),
            SVariable("?"),
            SVariable("0"),
            SVariable("1", 1),
            SVariable("state", initialState),

            # timer
            SVariable("millis"),
        ]

    def getCpp(self, identifier):
        """Return c++ code related to this conf."""
        if identifier == "include":
            return ["#include <SStd.h>"]
        elif identifier == "functions_all":
            return ["SSTD_FUNCTIONS_ALL"]
        return []
