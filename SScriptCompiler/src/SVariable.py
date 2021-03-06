"""Variable class for SScript."""
from src.SList import SList as sl


class SVariable:
    """class for SScript variables."""
    def __init__(self, name, value=0):
        """Set name and value"""
        self.name = name
        self.value = value  # initial value

    def getName(self):
        """Get the name of the variable."""
        return self.name

    def getValue(self):
        """Return name"""
        return self.value

    @staticmethod
    def create(variableNameValuePairs, states, confs, initialState="init"):
        """nameValuePairs -> [[variables(name, value)],[strings(name, value)]]."""
        variables = []
        if confs is not None:
            # get variables from the configurations used
            for conf in confs:
                variables += conf.getVariables({
                    "states": states,
                    "initialState": initialState
                })

        for variableNameValuePair in variableNameValuePairs:
            if type(variableNameValuePair) is tuple:
                # (name, value)
                variables.append(SVariable(
                    variableNameValuePair[0], variableNameValuePair[1]
                ))
            else:
                # name
                variables.append(SVariable(variableNameValuePair))
        # convert list of variables into SList and return it
        return sl(variables)
