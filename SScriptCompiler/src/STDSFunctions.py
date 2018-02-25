from src.SFunction     import SFunction     as sf
from src.SVariable     import SVariable     as sv
from src.SState        import SState        as ss
from src.SExpression   import SExpression   as se
from src.SList         import SList         as sl
from src.SCompiler     import SCompiler     as co

class STDSFunctions:
   def __init__(self, st = None, v = None):
      self.f = sl([
         # basic operations
         sf("+"),             # leftValue += righValue
         sf("-"),
         sf("/"),             # leftValue /= rightValue
         sf("*"),
         sf("="),             # leftValue = rightValue
         sf("<"),             # leftValue < rightValue
         sf(">"),             # leftValue > rightValue
         sf("=="),            # leftValue == rightValue
         # helper functions
         sf("access2pointer"), # set accessmode = pointer (for variables)
         sf("access2value"),   # set accessmode = value (for constants)
         sf("executeState"),   # currentState, currentElement = goto(state, element)
         sf("if"),            # (if rightValue != 0) execute, otherwise stop execution
         sf(";"),              # stop expression execution, do not set leftValue
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
      ]);
      self.st = st
      self.v = v

   def getAllSTDFunctions(self):
      return self.f

   # helper functions

   def executeState(self):
      """
      Execute state.

      Args:
          state (``str``): key by which the state is stored in SVariable[]
                            for now this is assumed
      """
      return se([self.v.get("state"), self.v.get("ZERO"), self.f.get("executeState")])

   def setState(self, state):
      return se([self.v.get("state"), self.v.get("ZERO"), self.f.get("access2value"),
         self.st.get(state), self.f.get("="), self.f.get("access2pointer")
      ])

   def setConditional(self, left, operator, right):
      # [?] = left operator right, e.g., 1 < 2
      return se([self.v.get("?"), self.v.get(left), self.f.get("="), self.v.get(right), self.f.get("<")])

   def conditionalSetState(self, state):
      # if ? != 0, set state
      return se([self.v.get("state"), self.v.get("?"), self.f.get("if"), self.v.get("ZERO"), self.f.get("access2value"),
         self.st.get(state), self.f.get("="), self.f.get("access2pointer")
      ])

   def readMPU(self):
      return se([self.v.get("tmp"), self.v.get("ONE"), self.f.get("mpu_readSensor")])

   def getTemperature(self):
      return se([self.v.get("temperature"), self.v.get("ONE"), self.f.get("mpu_getTemperature_C")])

   def printInt(self, i):
      return se([self.v.get(i), self.v.get("ZERO"), self.f.get("print")])

   def inc(self, i):
      return se([self.v.get(i), self.v.get("ONE"), self.f.get("+")])
