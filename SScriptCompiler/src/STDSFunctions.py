"""Helper module for accessing functions."""
from src.SFunction import SFunction as sf
from src.SVariable import SVariable as sv
from src.SState import SState as ss
from src.SExpression import SExpression as se
from src.SList import SList as sl
from src.SCompiler import SCompiler as co


class STDSFunctions:
    """Standard functions class for SScript."""

    def __init__(self,
                 stateNames=["main"],
                 variableNameValuePairs=None,
                 initialState="main",
                 useSTDVariables=True,
                 useSTDFunctions=True):
        """Set functions, states and variables."""

        self.st = ss.create(
            names=stateNames
        )

        self.v = sv.create(
            nameValuePairs=variableNameValuePairs,
            st=self.st,
            initialState=initialState,
            useSTDVariables=useSTDVariables)

        if useSTDFunctions:
            self.f = sl([
                # basic operations
                sf("+"),                # leftValue += righValue
                sf("-"),
                sf("*"),                # leftValue /= rightValue
                sf("/"),
                sf("="),                # leftValue = rightValue
                sf("<"),                # leftValue < rightValue
                sf(">"),                # leftValue > rightValue
                sf("=="),               # leftValue == rightValue
                # helper functions
                sf("executeState"),
                sf("if"),
                sf("else"),
                sf(";"),                # abort expression execution,
                sf("return"),           # abort state execution
                                        # leftvalue does not change
                # timer
                sf("readTimer"),
                sf("getTime"),
                sf("timeout"),

                # sensor
                sf("mpu_readSensor"),
                sf("mpu_getAccelX_mss"),
                sf("mpu_getAccelY_mss"),
                sf("mpu_getAccelZ_mss"),
                sf("mpu_getGyroX_rads"),
                sf("mpu_getGyroY_rads"),
                sf("mpu_getGyroZ_rads"),
                sf("mpu_getMagX_uT"),
                sf("mpu_getMagY_uT"),
                sf("mpu_getMagZ_uT"),
                sf("mpu_getTemperature_C"),
                # print (only int32_t for now)
                sf("printInt"),
                sf("printInt_ln"),
            ])

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
            (l = ["var", "var", "fun", "var", "fun", 1, "fun", 2])
        """

        expression = []

        # if there is only 1 element, it's a function
        if len(l) == 1:
            expression.append(self.get(self.f, l[0]))
            return se(expression)

        # if there are 2 elements, it's a set
        if len(l) == 2:
            # variable[l[0]] = l[1]
            # l[0] should always be variable, l[1] constant
            expression.append(self.get(self.v, l[0]))
            expression.append(self.get(self.v, l[1]))
            return se(expression)

        expression.append(self.get(self.v, l[0]))
        for i in range(1, len(l)):
            if i % 2 == 0:
                # function
                expression.append(self.get(self.f, l[i]))
            else:
                # variable
                if type(l[i]) is int:
                    # we do not want constat variables, thus
                    # add this "constant" as variable with value
                    # this could be inserter into either self.get or SList.get
                    # but we do not want all expressions
                    # (such as ["variable",value]) to be stored in memory,
                    # as there is no need to do so
                    self.v.append(sv(str(l[i]), int(l[i])))
                    l[i] = str(l[i])
                expression.append(self.get(self.v, l[i]))
        # convert expression into SExpression and return it
        return se(expression)

    def executeState(self):
        """Execute state."""
        return self.expr([
            "0", "state", "executeState"
        ])

    def readTimer(self):
        """Get time in ms."""
        return self.expr([
            "readTimer"
        ])

    def getTime(self, timeVariable):
        """Get time (which was stored when readTimer was last executed)."""
        return self.expr([
            timeVariable, "0", "getTime",
        ])

    def timeout(self, lastTimeout, length):
        """If timeout, abort state execution."""
        return self.expr([
            lastTimeout, length, "timeout"
        ])

    def _conditionalReturn(self):
        """Abort executing state, i.e., return from state."""
        return self.createIFELSE("if", ["tmp", "return"])

    def setState(self, state):
        """Set next_state = state."""
        return self.expr([
            "state", int(self.st.get(state))
        ])

    def set(self, name, value):
        """Set variable value.

        if constant:     variable[name].value = value.
        elif index:      variable[name].value = indexOf(value).
        else (value):    variable[name].value = variable[value].value.
        """

        if type(value) is int:
            # set constant
            return self.expr([
                name, value
            ])
        elif value[0] == "&":
            # set index (also constant)
            value = value[1:]
            return self.expr([
                name, value
            ])
        else:
            # set variable value
            #
            return self.expr([
                name, value, "="
            ])

    def setConditional(self, left, operator, right):
        """Set [?] = int(left < right)."""
        return self.expr([
            "?", left, "=", right, operator
        ])

    def eval(self, left, operator, right):
        """Short form for setConditional. may add additional f in future"""
        return self.setConditional(left, operator, right)

    def createIFELSE(self, evalF, expression):
        """insert evalIF ("if" or "else") into expression."""
        function = getattr(self, expression[0])
        args = expression[1:]
        _expression = function(*args)
        _expression = _expression.getList()
        _expression = [_expression[0], "?", evalF] + _expression[1:]
        _expression = self.expr(_expression)
        return _expression

    def IF(self, condition, expression_if, expression_else=None):
        """If condition: expression"""
        expressions = []
        # set condition
        function = getattr(self, condition[0])
        args = condition[1:]
        conditional = function(*args)
        expressions.append(conditional)
        # if
        _expression_if = self.createIFELSE("if", expression_if)
        expressions.append(_expression_if)
        # else
        if expression_else != None:
            _expression_else = self.createIFELSE("else", expression_else)
            expressions.append(_expression_else)
        return expressions

    def conditionalSetState(self, state):
        """If ? != 0, next_state = state."""
        # move new state into "tmp" variable
        state_new = self.expr([
            "tmp", int(self.st.get(state))
        ])
        # set state if conditional != 0
        conditional_set = self.expr([
            "state", "?", "if", "tmp", "="
        ])
        # return the expression [subexpression1, subexpression2]
        return [state_new, conditional_set]

    def readMPU(self, errorVariable=None):
        """Read the mpu sensor."""
        if errorVariable is None:
            return self.expr([
                "mpu_readSensor"
            ])
        else:
            return self.expr([
                errorVariable, "1", "mpu_readSensor"
            ])

    def getMpuValue(self, identifier, multiplier=1):
        """Read sensor value to matching stdVariable."""
        return self.expr([
            identifier, str(multiplier), "mpu_get" + identifier
        ])

    def printInt(self, i, endl=False):
        """Print variable as integer to serial port."""
        if endl:
            return self.expr([
                "0", i, "printInt_ln"
            ])
        else:
            return self.expr([
                "0", i, "printInt"
            ])

    def inc(self, i):
        """Increase variable value by one."""
        return self.expr([
            i, "1", "+"
        ])
