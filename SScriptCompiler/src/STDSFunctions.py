from src.SFunction import SFunction as sf

class STDSFunctions:
   def __init__(self):
      self.STDFunctions = [
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
      ];

   def getAllSTDFunctions(self):
      return self.STDFunctions
