class SList:
   def __init__(self, value):
      self.value = value

   def get(self, name):
      for i, val in enumerate(self.value):
         if val.name == name:
            return str(i)
      print ("Error: " + name + " Not found in " + str(val))
      raise NameError

   def getValue(self):
       return self.value

   def getLen(self):
      return len(self.value)
