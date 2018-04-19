import sys
from collections import OrderedDict

# SScript
from src.SProgram import SProgram as program
from .common import flattenList


class SComposite:

    def __init__(self, compositeData):
        self.compositeData = compositeData
        if len(self.compositeData) == 0:
            sys.exit(2)

        self.programData = self.compositeData['programData']
        self.programCount = len(self.programData)

    def doShare(self):
        shared = self.compositeData['shared']
        for identifier in shared:
            for programNames in shared[identifier]:
                lst = []
                for programName in programNames:
                    lst += self.programData[programName][identifier]

                lst = flattenList(lst)
                # instead of set, use OrderedDict, as it quaramtees the order
                #   (order is imporant in function indexing (i.e. at least confs))
                lst = list(OrderedDict.fromkeys(lst))

                for programName in programNames:
                    self.programData[programName][identifier] = lst

    def doCompile(self):
        self.compiled = []
        for programName in self.programData:
            p = program(**self.programData[programName])
            self.compiled.append(p.compile())

    def doPrint(self):
        print("\n" + "*"*20 + "\nC++ template code (composite)\n"+ "*"*20 + "\n")

        # includes (force shared for peformance and memory)
        print(self.compiled[0]['cppIncludes_str'])
        # functions (force shared for peformance and memory)
        print(self.compiled[0]['cppFunctionsAll_str'])

        print("\nSScript _sScript[" + str(self.programCount) + "]")
        print("void(*(*_functions))() = functions;")

        # setup
        print("\nvoid setup() {")
        print("   for (int i = 0; i < " + str(self.programCount) + "; i++) {")
        print("      _sScript[i].setFunctions(_functions);")
        print("   }")
        print("   // configure (TODO: may require compiler & interpreter modifications)")
        print("}")

        # loop
        print("\nvoid loop() {")
        print("   for (int i = 0; i < " + str(self.programCount) + "; i++) {")
        print("      sScript = &_sScript[i];")
        print("      sScript->loop();")
        print("   }")
        print("}")

        # main
        print("\nint main(int argc, char* argv[]) {\n")
        print("   // Execute.")
        print("   while (true) {")
        print("      loop();")
        print("   }\n")
        print("}")

    def compile(self):
        self.doShare()
        self.doCompile()
        self.doPrint()
