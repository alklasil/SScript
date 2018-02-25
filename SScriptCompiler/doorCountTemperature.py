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

   # states
   st = sl([
      sf("main"), sf("init"), sf(">t"), sf("<t>"), sf("<t"),
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

   # functions
   f = stdf(st, v)

   s = sl([
      # main state always first
      ss("main", [
         # goto execute the sate set by variable "state"
         f.executeState(),
      ]),
      ss("init", [
         # calibrate (thresholds), set tUP and tDOWN & only then set state = "process"
         # (TODO)

         # set state = '>t' (above threshold)
         f.setState(">t")

      ]),
      ss(">t", [
         # read mpu sensor
         f.readMPU(),

         # get temperature
         f.getTemperature(),

         # [?] = temperature < tDOWN
         f.setConditional("temperature", "<", "tDOWN"),

         # if [?] state = "<t>" for processing
         f.conditionalSetState("<t>"),
      ]),
      ss("<t>", [
         # state = "closing the door", do not execute when opening the door
         # increase count by one
         f.inc("count"),
         # "debug" print the increased value
         f.printInt("count"),
         # set state
         f.setState(">t")
      ]),
      ss("<t", [
         # read mpu sensor
         f.readMPU(),

         # get temperature
         f.getTemperature(),

         # [?] = temperature > tDOWN
         f.setConditional("temperature", ">", "tDOWN"),

         # if [?] state = "<t"
         f.conditionalSetState(">t")
      ]),
   ])

   c = co(s, f, v)

   print( c.compile() )

if __name__ == "__main__":
    # execute only if run as a script
    main()
