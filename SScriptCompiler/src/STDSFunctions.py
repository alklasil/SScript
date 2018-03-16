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

        # if there is only 1 element, it's a function
        # (This already works in 0.2)
        if len(l) == 1:
            expression.append(self.get(self.f, l[0]))
            return se(expression)

        # if there are 2 elements, it's a set

        # This is not allowed in 0.2 anymore, use set("=") instead
        # TODO: clean up other places, where ts related to this may appear
        #if len(l) == 2:
        #    # variable[l[0]] = l[1]
        #    # l[0] should always be variable, l[1] constant
        #    expression.append(self.get(self.v, l[0]))
        #    expression.append(self.get(self.v, l[1]))
        #    return se(expression)

        # expression.append(self.get(self.v, l[0]))
        # for now: fun, var, var, fun, var, var, fun, var, var
        # TODO 0.2: allow free order
        for i in range(0, len(l)):
            if i % 3 == 0:
                # function
                expression.append(self.get(self.f, l[i]))
            else:
                # variable
                expression.append(self.get(self.v, l[i]))
        # convert expression into SExpression and return it
        return se(expression)

    def executeState(self, var="state"):
        """Execute state."""
        return self.expr([
            "executeState", "0", var
        ])

    def readTimer(self):
        """Get time in ms."""
        return self.expr([
            "readTimer"
        ])

    def getTime(self, timeVariable):
        """Get time (which was stored when readTimer was last executed)."""
        return self.expr([
            "getTime", timeVariable, "0"
        ])

    def timeout(self, lastTimeout, length):
        """If timeout, abort state execution."""
        return self.expr([
            "timeout", lastTimeout, length
        ])

    def conditionalReturn(self):
        """Abort executing state, i.e., return from state."""
        return self.createIFELSE("if", ["tmp", "return"])

    def setState(self, state, var="state"):
        """Set next_state = state."""
        return self.expr([
            "=(const)=", var, int(self.st.get(state))
        ])

    def set(self, name, value):
        """Set variable value.

        if constant:     variable[name].value = value.
        elif index:      variable[name].value = indexOf(value).
        else (value):    variable[name].value = variable[value].value.
        """
        # print ("set value:", value)
        if type(value) is int:
            # set constant
            # print ("set constant:", value)
            return self.expr([
                "=(const)=", name, value
            ])
        elif value[0] == "&":
            # set index (also constant)
            value = value[1:]
            return self.expr([
                "=(const)=", name, value
            ])
        else:
            # set variable value
            return self.expr([
                "=", name, value
            ])

    def setConditional(self, left, operator, right):
        """Set [?] = int(left operator right), e.g., left < right."""
        return self.expr([
            "=", "?", left, operator, "?", right
        ])

    def conditionalSetState(self, state):
        """If ? != 0, next_state = state."""
        # move new state into "tmp" variable
        #state_new = self.expr([
        #    "=(const)=", "tmp", int(self.st.get(state))
        #])
        # set state if conditional != 0
        return self.expr([
            "if", "0", "?",
            "=(const)=", "state", int(self.st.get(state))
        ])
        # return the expression [subexpression1, subexpression2]
        #return [state_new, conditional_set]

    def readMPU(self, errorVariable=None):
        """Read the mpu sensor."""
        if errorVariable is None:
            return self.expr([
                "mpu_readSensor"
            ])
        else:
            return self.expr([
                "mpu_readSensor", errorVariable, "1"
            ])

    def getMpuValue(self, identifier, multiplier=1):
        """Read sensor value to matching stdVariable."""
        return self.expr([
            "mpu_get" + identifier, identifier, str(multiplier)
        ])

    def printInt(self, i, endl=False):
        """Print variable as integer to serial port."""
        if endl:
            return self.expr([
                "printInt_ln", "0", i
            ])
        else:
            return self.expr([
                "printInt", "0", i
            ])

    def printString(self, i, endl=False):
        """Print string to serial port."""
        if endl:
            return self.expr([
                "printString_ln", "0", i
            ])
        else:
            return self.expr([
                "printString", "0", i
            ])

    def clearString(self, var):
        """Var = ''."""
        return self.expr([
            "clearString", var, "0"
        ])

    def concatString_String(self, leftValue, rightValue):
        """LeftValue += rightValue."""
        return self.expr([
            "concatString_String", leftValue, rightValue
        ])

    def concatString_Int(self, leftValue, rightValue):
        """LeftValue += str(rightValue)."""
        return self.expr([
            "concatString_Int", leftValue, rightValue
        ])

    def inc(self, i):
        """Increase variable value by one."""
        return self.expr([
            "+", i, "1"
        ])
