"""Compiler module for SScript."""


class SCompiler:
    """Compiler class for SScript."""
    def __init__(self, s, f, v):
        """Set states, functions and variables."""
        self.s = s
        self.f = f
        self.v = v
        self.compiled = []

    def compile(self):
        """Compile SScript."""
        v = self.v
        f = self.f
        s = self.s

        c = []  # = self.compiled
        # number of variables
        c.append(str(v.getLen()))
        # initialize values (number of values to initialize)
        num = 0  # number/count of values to initialize
        for vi, variable in enumerate(v.getValue()):
            if variable.getValue() != 0:
                num += 1
        c.append(str(num))
        # initialize values (initialize values)
        for vi, variable in enumerate(v.getValue()):
            if variable.getValue() != 0:
                c.append(str(vi))
                c.append(str(variable.getValue()))
        # number of states
        c.append(str(s.getLen()))
        # states::expressions
        for si, state in enumerate(s.getValue()):
            # number of expressions in state
            c.append(str(state.getLen()))
            for ei, expression in enumerate(state.getExpressions()):
                # number of elements in expression
                c.append(str(expression.getLen()))
                c.append(expression.get())

        self.compiled = c
        return self.getCompiled()

    def getCompiled(self):
        """Get the compiled SScript as string"""
        return ' '.join(self.compiled)
