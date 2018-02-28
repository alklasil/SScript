"""Helper module for accessing functions."""
from src.SFunction import SFunction as sf
from src.SVariable import SVariable as sv
from src.SState import SState as ss
from src.SExpression import SExpression as se
from src.SList import SList as sl
from src.SCompiler import SCompiler as co


class STDSFunctions:
    """Standard functions class for SScript."""

    def __init__(self, st=None, v=None):
        """Set functions, states and variables."""
        self.f = sl([
            # basic operations
            sf("+"),             # leftValue += righValue
            sf("-"),
            sf("*"),             # leftValue /= rightValue
            sf("/"),
            sf("="),             # leftValue = rightValue
            sf("<"),             # leftValue < rightValue
            sf(">"),             # leftValue > rightValue
            sf("=="),            # leftValue == rightValue
            # helper functions
            sf("access2pointer"),  # set accessmode = pointer (for variables)
            sf("access2value"),   # set accessmode = value (for constants)
            sf("executeState"),
            # currentState, currentElement = goto(state, element)
            # (if rightValue != 0) execute, otherwise stop execution
            sf("if"),
            sf(";"),              # abort expression execution,
                                  # leftvalue does not change
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
            sf("print"),
        ])
        self.st = st
        self.v = v

    def getAllSTDFunctions(self):
        """Return standard functions."""
        return self.f

    # helper functions

    def expr(self, l):
        """Enable simpler expression creation.

        Args:
            l = str[] (list of strings [states, variables, functions]
            (l = ["var", "var", "fun", "var", "fun", 1, "fun", 2])
        """
        expression = []

        # if there is only 1 element, it's a function
        if len(l) == 1:
            expression.append(self.f.get(l[0]))
            return se(expression)

        # if there are 2 elements, it's a set
        if len(l) == 2:
            # the first is always a variable
            expression.append(self.v.get(l[0]))
            # the second is always a constant
            expression.append(str(l[1]))

            return se(expression)

        # if there are >= 3 elements, it's a normal expression
        # first variable is always a variable, never a constant
        expression.append(self.v.get(l[0]))
        for i in range(1, len(l)):
            s = l[i]
            # if element is str, get it's index, otherwise it's a constant
            if isinstance(s, str):
                # if i % 2 == 0, it's a function
                if i % 2 == 0:
                    s = self.f.get(l[i])
                # otherwise it's a variable
                else:
                    s = self.v.get(l[i])
            # add the element into the expression
            expression.append(str(s))

        # convert expression into SExpression and return it
        return se(expression)

    def executeState(self):
        """Execute state."""
        return self.expr([
            "0", "state", "executeState"
        ])

    def setState(self, state):
        """Set next_state = state."""
        return self.expr([
            "state", int(self.st.get(state))
        ])

    def setConditional(self, left, operator, right):
        """Set [?] = int(left < right)."""
        return self.expr([
            "?", left, "=", right, "<"
        ])

    def conditionalSetState(self, state):
        """If ? != 0, next_state = state."""
        return self.expr([
            "state", "?", "if", "0", "access2value",
            int(self.st.get(state)), "=", "0", "access2pointer"
        ])

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

    def printInt(self, i):
        """Print variable as integer to serial port."""
        return self.expr([
            "0", i, "print"
        ])

    def inc(self, i):
        """Increase variable value by one."""
        return self.expr([
            i, "1", "+"
        ])
