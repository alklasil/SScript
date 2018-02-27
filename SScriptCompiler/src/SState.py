from src.SFunction     import SFunction     as sf

class SState:
   def __init__(self, name, expressions):
      self.name = name
      self.expressions = expressions

   def getExpressions(self):
      return self.expressions

   def getLen(self):
      return len(self.expressions)

   @staticmethod
   def stdStates():
        return [
            SState("_main")
        ]
