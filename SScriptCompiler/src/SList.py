"""List module for SScript."""


class SList:
    """List class for SScript."""

    def __init__(self, value):
        """Set value (anything[])."""
        self.value = value

    def append(self, val, listIndex=0):
        """Append value into self.value."""
        # append only if a value with the name does not already exist

        for v in self.value[listIndex]:
            if v.name == val.name:
                return False
        self.value[listIndex].append(val)
        return True

    def get(self, name):
        """Get index ('address') by name."""
        # check if it is a pointer
        isPointer = False
        if name[0] == "*":
            isPointer = True

        value = self.value
        if not type(value[0]) is list:
            value = [value]

        for vi, subvalue in enumerate(value):
            for i, val in enumerate(subvalue):
                if isPointer and val.name == name[1:]:
                    if hasattr(val, "value"):
                        # it's variable pointer,
                        # functions do not have value
                        # pointers are negative indexes (-1 points to 1)
                        return "-" + str(i)
                if val.name == name:
                    return str(i)

        try:
            # test if it's a number, may or may not have already been converted
            # we want to test this last, because numbers can be variables
            i = int(name)
            return str(name)
        except ValueError:
            print ("raised NameError:" + name + " Not found in " + str(val))
            raise NameError

    def getValue2SLists(self):
        """Get value, for which is assumed type(value) = [[]]."""
        return [
            SList(l)
            for l in self.value
        ]

    def getValue(self):
        """Get value."""
        return self.value

    def getLen(self):
        """Get length of value[]."""
        return len(self.value)

    def getNames(self, listIndex=0):

        return [
            val.getName()
            for val in self.values[listIndex]
        ]
