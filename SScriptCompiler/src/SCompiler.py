"""Compiler module for SScript."""


class SCompiler:
    """Compiler class for SScript."""
    def __init__(self, p):
        """Set states, functions and variables."""
        self.s = p.getSoftware()
        self.f = p.getFunctions()
        self.v = self.f.getVariables()
        self.compiled = []

    def compile(self):
        """Compile SScript."""
        v = self.v
        f = self.f
        s = self.s

        print("\nCOMPILING...\n")

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
        print("states:" + str(s.getLen()))
        c.append(str(s.getLen()))
        # states::expressions
        for si, state in enumerate(s.getValue()):
            # parse subexpressions
            _expressions = []
            for expression in state.getExpressions():
                if type(expression) is list:
                    for subexpression in expression:
                        _expressions.append(subexpression)
                else:
                    _expressions.append(expression)
            # reset expressions
            state.set(_expressions)
            # number of expressions in state
            print(" state(" + str(si) + ") expressions: "
                  + str(state.getLen()))
            c.append(str(state.getLen()))
            for ei, expression in enumerate(state.getExpressions()):
                # number of elements in expression
                print("   expression(" + str(ei) + ") elements: "
                      + str(expression.getLen()))
                c.append(str(expression.getLen()))
                c.append(expression.get())

        print("\nCOMPILED...\n")

        self.compiled = c
        return self.getCompiled()

    def getCompiled(self):
        """Get the compiled SScript as string"""
        return ' '.join(self.compiled)
