"""Compiler module for SScript."""


class SCompiler:
    """Compiler class for SScript."""
    def __init__(self, p):
        """Set states, functions and variables."""
        self.p = p

    def compile(self):
        """Compile SScript."""
        print("\nCOMPILING...\n")

        c = []  # = self.compiled

        # number of variables
        c.append(self.p.sVariables.getLen())
        # initialize values (number of values to initialize)
        num = 0  # number/count of values to initialize
        for vi, variable in enumerate(self.p.sVariables.getValue()):
            if variable.getValue() != 0:
                num += 1
        c.append(str(num))
        # initialize values (initialize values)
        for vi, variable in enumerate(self.p.sVariables.getValue()):
            if variable.getValue() != 0:
                c.append(str(vi))
                c.append(str(variable.getValue()))

        # number of strings
        c.append(str(self.p.sStrings.getLen()))

        # initialize values (number of values to initialize)
        num = 0  # number/count of values to initialize
        for si, s1 in enumerate(self.p.sStrings.getValue()):
            if s1.getValue() != "":
                num += 1
        c.append(str(num))
        # initialize values (initialize values)
        for si, s1 in enumerate(self.p.sStrings.getValue()):
            if s1.getValue() != "":
                c.append(str(si))
                c.append(str(s1.getValue()) + ";")

        # number of states
        print("states:" + str(self.p.sStates.getLen()))
        c.append(str(self.p.sStates.getLen()))
        # states::expressions
        for si, state in enumerate(self.p.sStates.getValue()):
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
                      + str(expression.getLen())
                      + " [" + str(expression.get()) + "]")
                c.append(str(expression.getLen()))
                c.append(expression.get())

        self.compiled = c

        # print c++ template code
        self.printCpp()

        print("\nCOMPILED...\n")
        return self.getCompiled()

    def getCompiled(self):
        """Get the compiled SScript as string"""
        return ' '.join([
            str(element)
            for element in self.compiled
        ])

    def printCpp(self):
        # print c++ template code
        cppIncludes = []
        cppFunctionsAll = []
        for conf in self.p.sConfs:
            if hasattr(conf, "getCpp"):
                cppIncludes = cppIncludes + conf.getCpp("include")
                cppFunctionsAll = cppFunctionsAll + conf.getCpp("functions_all")

        print("\n" + "*"*20 + "\nC++ template code\n"+ "*"*20 + "\n")
        print("\n".join(cppIncludes))
        print("\nvoid(*functions[])() = {")
        print("   " + ",\n   ".join(cppFunctionsAll))
        print("}")
        print("\nint main(int argc, char* argv[]) {\n")
        print("   // create SScript instance & set sScript to point to the created instance.")
        print("   //    To switch between different sScript instances, simply point sScript to a different instance")
        print("   SScript _sScript;")
        print("   sScript = &_sScript;\n")
        print("   // Set functions.")
        print("   void(*(*_functions))() = functions;")
        print("   sScript->setFunctions(_functions);\n")
        print("   // Configure.")
        print('   char *buffer = "' + self.getCompiled() + '"')
        print("   sScript->set(buffer);\n")
        print("   // Execute.")
        print("   while (true) {")
        print("      sScript->loop();")
        print("   }\n")
        print("}")
