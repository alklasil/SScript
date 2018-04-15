import sys
from collections import OrderedDict

# SScript
from src.SProgram import SProgram as program
from .common import flattenList

class SComposite:

    def __init__(self, compositeData):
        self.compositeData = compositeData

    def compile(self):

        if len(self.compositeData) == 0:
            sys.exit(2)

        programData = self.compositeData['programData']
        shared = self.compositeData['shared']

        for identifier in shared:
            for programNames in shared[identifier]:
                lst = []
                for programName in programNames:
                    lst += programData[programName][identifier]

                lst = flattenList(lst)
                # instead of set, use OrderedDict, as it quaramtees the order
                #   (order is imporant in function indexing (i.e. at least confs))
                lst = list(OrderedDict.fromkeys(lst))

                for programName in programNames:
                    programData[programName][identifier] = lst

        # compile
        for programName in programData:
            p = program(**programData[programName])
            p.compile()
