"""Compiler module for SScript."""

class SCompiler:
    """Compiler class for SScript."""
    def __init__(self, p):
        """Set states, functions and variables."""
        self.p = p
        self.data = {}
        self.data["compiled"] = []
        self.data["info"] = {}

    def doInitializeElements(self, elements, defaultVal, delimiter=None):
        # number of elements
        self.data["compiled"].append(elements.getLen())
        # count how many elements to initialize
        num = 0
        for i, element in enumerate(elements.getValue()):
            if element.getValue() != defaultVal:
                num += 1
        self.data["compiled"].append(str(num))
        # initialize
        for i, element in enumerate(elements.getValue()):
            if element.getValue() != defaultVal:
                self.data["compiled"].append(str(i))
                if delimiter is None:
                    self.data["compiled"].append(str(element.getValue()))
                else:
                    self.data["compiled"].append(str(element.getValue()) + delimiter)

    def doInitializeVariables(self):
        self.doInitializeElements(self.p.sVariables, 0)

    def doInitializeStrings(self):
        self.doInitializeElements(self.p.sStrings, "", ";")

    def doInitializeStates(self):
        # number of states
        print("states:" + str(self.p.sStates.getLen()))
        self.data["compiled"].append(str(self.p.sStates.getLen()))
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
            self.data["compiled"].append(str(state.getLen()))
            for ei, expression in enumerate(state.getExpressions()):
                # number of elements in expression
                print("   expression(" + str(ei) + ") elements: "
                      + str(expression.getLen())
                      + " [" + str(expression.get()) + "]")
                self.data["compiled"].append(str(expression.getLen()))
                self.data["compiled"].append(expression.get())

    def doInfo(self):
        cppIncludes = []
        cppFunctionsAll = []
        for conf in self.p.sConfs:
            if hasattr(conf, "getCpp"):
                cppIncludes = cppIncludes + conf.getCpp("include")
                cppFunctionsAll = cppFunctionsAll + conf.getCpp("functions_all")

        self.data["info"]['cppIncludes'] = cppIncludes
        self.data["info"]['cppIncludes_str'] = "\n".join(self.data["info"]['cppIncludes'])

        self.data["info"]['cppFunctionsAll'] = cppFunctionsAll
        self.data["info"]['cppFunctionsAll_str'] = "\nvoid(*functions[])() = {\n   "
        self.data["info"]['cppFunctionsAll_str'] += ",\n   ".join(self.data["info"]['cppFunctionsAll'])
        self.data["info"]['cppFunctionsAll_str'] += "\n}"

        self.data["info"]['compiled'] = self.data['compiled']
        self.data["info"]['compiled_str'] = ' '.join([
            str(element)
            for element in self.data["compiled"]
        ])

    def compile(self):
        """Compile SScript."""
        print("\nCOMPILING...\n")

        self.doInitializeVariables()

        self.doInitializeStrings()

        self.doInitializeStates()

        self.doInfo()

        self.printCpp()

        print("\nCOMPILED...\n")

        return self.getCompiled()

    def getCompiled(self):
        """Get the compiled SScript as string"""
        return self.data["info"]

    def printCpp(self):
        print("\n" + "*"*20 + "\nC++ template code\n"+ "*"*20 + "\n")
        print(self.data["info"]['cppIncludes_str'])

        print(self.data["info"]['cppFunctionsAll_str'])

        print("\nvoid setup() {")
        print("   // create SScript instance & set sScript to point to the created instance.")
        print("   //    To switch between different sScript instances, simply point sScript to a different instance")
        print("   SScript _sScript;")
        print("   sScript = &_sScript;\n")
        print("   // Set functions.")
        print("   void(*(*_functions))() = functions;")
        print("   sScript->setFunctions(_functions);\n")
        print("   // Configure.")
        print('   char *buffer = "' + self.getCompiled().get('compiled_str') + '"')
        print("   sScript->set(buffer);\n")
        print("}")

        print("\nvoid loop() {")
        print("      sScript->loop();")
        print("}")

        print("\nint main(int argc, char* argv[]) {\n")
        print("   // Execute.")
        print("   while (true) {")
        print("      loop();")
        print("   }\n")
        print("}")
