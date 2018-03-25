"""Helper module for accessing functions."""
from src.SVariable import SVariable as sv
from src.SState import SState as ss
from src.SExpression import SExpression as se
from src.SList import SList as sl
from src.conf.std import Std as Std


class STDSFunctions:
    """Standard functions class for SScript."""

    def __init__(self,
                 stateNames=["main"],
                 nameValuePairs=None,
                 initialState="main",
                 confs=[Std()]):
        """Set functions, states and variables."""

        self.st = ss.create(
            names=stateNames
        )

        self.v = sv.create(
            nameValuePairs=nameValuePairs,
            st=self.st,
            confs=confs,
            initialState=initialState)

        # get functions in different configurations
        self.f = []
        for conf in confs:
            self.f += conf.getFunctions()
        self.f = sl(self.f)

    def getAllSTDFunctions(self):
        """Return standard functions."""
        return self.f

    def getStates(self):
        """Return all states."""
        return self.st

    def getState(self, state="state"):
        """Return state index."""
        return int(self.st.get(state))

    def getVariables(self):
        """Return all variables."""
        return self.v

    def get(self, sList, s):
        """Get variable or function."""
        try:
            # either 'integer' or 'variable'
            _s = sList.get(s)
        except (TypeError):
            # was constant (or at least that is assumed for now)
            # will raise other errors later, if that was not the case
            _s = str(s)
        return _s

    # helper functions
    #   all helper functions return either:
    #       se(expression) or se(expression)[]

    def expr(self, l):
        """Enable simpler expression creation.

        Args:
            l = str[] (list of strings [states, variables, functions]
            (l = ["fun", "var", "var", "var", "fun", 1, "fun"])
        """

        expression = []
        for element in l:
            # print(element)
            if type(element) is str and element[0] == '$':
                # function
                expression.append(self.get(self.f, element[1:]))
            elif type(element) is str and element[0] == '@':
                expression.append(self.st.get(element[1:]))
            else:
                # variable
                expression.append(self.get(self.v, element))
        # convert expression into SExpression and return it
        return se(expression)
