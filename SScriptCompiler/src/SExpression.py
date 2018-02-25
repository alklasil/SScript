class SExpression:
   def __init__(self, value):
       self.value = value

   def get(self):
       return ' '.join(self.value)

   def getLen(self):
       return len(self.value)
