class SVariable:
   def __init__(self, name, value=0):
      self.name = name
      self.value = value # initial value

   def getValue(self):
      return self.value

      # stdVariables
   @staticmethod
   def stdVariables(st, intialState = "main"):
        return [
             # basic variables
             SVariable("?"),
             SVariable("tmp"),
             SVariable("ZERO"), SVariable("ONE", 1),
             SVariable("state", st.get(intialState)),

             # sensor variables
             # accelerometer
             SVariable("mpu_accelX_mss"),             # amplitude in x-direction
             SVariable("mpu_accelZ_mss"),             # amplitude in z-direction
             SVariable("mpu_accelY_mss"),             # amplitude in y-direction
             SVariable("mpu_accel_mss"),              # amplitude of [x,y,z]

             # gyroscope
             SVariable("mpu_gyroX_rads"),
             SVariable("mpu_gyroY_rads"),
             SVariable("mpu_gyroZ_rads"),
             SVariable("mpu_gyro_rads"),

             # magnetometer
             SVariable("mpu_magY_uT"),
             SVariable("mpu_magX_uT"),
             SVariable("mpu_magZ_uT"),
             SVariable("mpu_mag_uT"),

             # temperature
             SVariable("mpu_temperature_C"),
          ]
