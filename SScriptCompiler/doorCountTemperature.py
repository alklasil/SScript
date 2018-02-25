from src.SFunction     import SFunction     as sf
from src.STDSFunctions import STDSFunctions as stdf
from src.SVariable     import SVariable     as sv
from src.SState        import SState        as ss
from src.SExpression   import SExpression   as se
from src.SList         import SList         as sl
from src.SCompiler     import SCompiler     as co

# DESCRIPTION:
#   This script calculates how many times a door has been opened based on temperature changes.
#   steps:
#       (1) init: calibrate temperature sensor (set 2 thresholds (outside vs inside)) TOOD
#       (2) process:
#               (2.1) measure sensor values
#               (2.2) compare values to thresholds, if open and below threshold,
#                     count++, state = below, back when above threshold
#


def main():

   # functions
   f = sl(
      stdf().getAllSTDFunctions()
   );

   # states
   st = sl([
      sf("main"), sf("init"), sf(">t"), sf("<t"),
   ]);

   # variables
   v = sl([
      sv("temperature"),                # = door opened "count" times
      sv("count"),                      # = door opened "count" times
      sv("tUP", 15),                    # threshold up (assume roomTemperature > 15)
      sv("tDOWN", 10),                  # threshold down (assume outsideTemperature < 10)
      sv("ZERO", 0),                    # constant(0), fast access
      sv("ONE", 1),                     # constant(1), fast access
      sv("state", st.get("init")),      # first state is "init" state
      sv("?", 0),                       # variable, used to store the result of conditional calculations
      sv("tmp")                         # bin
   ]);

   s = sl([
      # main state always first
      ss("main", [
         # goto execute the sate set by variable "state"
         se([v.get("state"), v.get("ZERO"), f.get("executeState")]),
      ]),
      ss("init", [
         # calibrate (thresholds), set tUP and tDOWN & only then set state = "process"
         # (TODO)

         # set state = '>t' (above threshold)
         se([v.get("state"), v.get("ZERO"), f.get("access2value"),
           st.get(">t"), f.get("="), f.get("access2pointer")
         ]),
      ]),
      ss(">t", [
         # read mpu sensor
         se([v.get("tmp"), v.get("ONE"), f.get("mpu_readSensor")]),

         # get temperature
         se([v.get("temperature"), v.get("ONE"), f.get("mpu_getTemperature_C")]),

         # ? = temperature < tDOWN
         se([v.get("?"), v.get("tDOWN"), f.get("="), v.get("temperature"), f.get("<")]),

         # if ? != 0, i.e., temperature < tDOWN: state = "<t"
         se([v.get("state"), v.get("?"), f.get("if"), v.get("ZERO"), f.get("access2value"),
           st.get("<t"), f.get("="), f.get("access2pointer")
         ]),

         se([v.get("count"), v.get("ONE"), f.get("+")]),
         se([v.get("count"), v.get("ZERO"), f.get("print")])
      ]),
      ss("<t", [
         # read mpu sensor
         se([v.get("tmp"), v.get("ONE"), f.get("mpu_readSensor")]),

         # get temperature
         se([v.get("temperature"), v.get("ONE"), f.get("mpu_getTemperature_C")]),

         # ? = temperature > tUP
         se([v.get("?"), v.get("tUP"), f.get("="), v.get("temperature"), f.get(">")]),

         # if ? != 0, i.e., temperature > tUP: state = ">t"
         se([v.get("state"), v.get("?"), f.get("if"), v.get("ZERO"), f.get("access2value"),
           st.get(">t"), f.get("="), f.get("access2pointer")
         ]),

         # do not add door opened count here, as we already did when opening the door
      ]),

   ])

   c = co(s, f, v)

   print( c.compile() )

if __name__ == "__main__":
    # execute only if run as a script
    main()
