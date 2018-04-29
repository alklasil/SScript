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

        self.programCount = len(self.compositeData)
        self.setupData = {}

    def doShare(self):

        # create share dict
        shared = {}
        for programName in self.compositeData:
            for identifier in self.compositeData[programName]:
                if identifier == 'programData':
                    pass
                else:
                    # shared (masterName = master/owner of the shared data)
                    masterName = self.compositeData[programName][identifier]
                    if identifier not in shared:
                        # identifier not yet in shared dict -> create
                        shared[identifier] = {masterName: [masterName, programName]}
                    else:
                        if masterName not in shared[identifier]:
                            # new slave to a new master
                            shared[identifier][masterName] = [masterName, programName]
                        else:
                            # new slave to an existing master
                            shared[identifier][masterName] = shared[identifier][masterName] + [programName]

        for identifier in shared:
            for masterName in shared[identifier]:
                programNames = shared[identifier][masterName]
                lst = []
                for programName in programNames:
                    lst += self.compositeData[programName]['programData'][identifier]

                lst = flattenList(lst)
                # instead of set, use OrderedDict, as it quaramtees the order
                #   (order is imporant in function indexing (i.e. at least confs))
                lst = list(OrderedDict.fromkeys(lst))

                for programName in programNames:
                    self.compositeData[programName]['programData'][identifier] = lst

    def doCompile(self):
        self.compiled = {}
        for programName in self.compositeData:
            p = program(**self.compositeData[programName]['programData'])
            self.compiled[programName] = p.compile()

    def doSetupOne(self, one):
        if one == 'variables':
            allocate = 'allocateVariables'
            initialize = 'initializeVariables'
            identifier = 'variableNameValuePairs'
        elif one == 'strings':
            allocate = 'allocateStrings'
            initialize = 'initializeStrings'
            identifier = 'stringNameValuePairs'
        elif one == 'states':
            allocate = 'allocateStates'
            initialize = 'initializeStates'
            identifier = 'states'
        else:
            return

        elements = one + "." + identifier

        def setup(programName):
            print("   sScript = &_sScript[" + programName + "]);")
            SScriptName = "_sScript[" + programName + "]"
            if identifier not in self.compositeData[programName]:
                # master
                print("   " + SScriptName + "." + allocate + "();")
            else:
                # slave
                masterSScriptName = "_sScript[" + self.compositeData[programName][identifier] + "]"
                print("   " + SScriptName + "." + allocate + "(" + masterSScriptName + "." + one + ");")

        print("\n   // setup " + one)
        # setup masters
        for programName in self.compositeData:
            if identifier not in self.compositeData[programName]:
                setup(programName)
        # setup slaves (i.e. the ones that are not masters)
        for programName in self.compositeData:
            if identifier in self.compositeData[programName]:
                setup(programName)

    def doSetup(self):
        self.doSetupOne('variables')
        self.doSetupOne('strings')
        self.doSetupOne('states')

    def doPrint(self):
        print("\n" + "*"*20 + "\nC++ template code (composite)\n"+ "*"*20 + "\n")

        compiled_one = list(self.compiled.values())[0]
        # includes (force shared for peformance and memory)
        print(compiled_one['cppIncludes_str'])
        # functions (force shared for peformance and memory)
        print(compiled_one['cppFunctionsAll_str'])

        i = 0
        print("")
        for programName in self.compositeData:
            print("#define " + programName + " " + str(i))
            i = i + 1

        print("\n// compiled_str")

        for programName in self.compositeData:
            print("\nchar * " + programName + '_str = "' + self.compiled[programName]['compiled_str'] + '";')
            i = i + 1

        print("\nSScript _sScript[" + str(self.programCount) + "]")
        print("void(*(*_functions))() = functions;")

        # setup
        print("\nvoid setup() {")
        print("   // TODO: enable do not force conf sharing, would this be useful?")
        print("   //       if not, force confs sharing in compositeData automatically instead of manual as is for now")
        print("   for (int i = 0; i < " + str(self.programCount) + "; i++) {")
        print("      _sScript[i].setFunctions(_functions);")
        print("   }")
        print("   // set str")
        for programName in self.compositeData:
            print("   " + programName + ".setStr(" + programName + "_str);")
        self.doSetup()
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
