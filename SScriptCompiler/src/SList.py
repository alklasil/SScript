"""List module for SScript."""


class SList:
    """List class for SScript."""

    def __init__(self, value):
        """Set value (anything[])."""
        self.value = value

    def append(self, val):
        """Append value into self.value."""
        # append only if a value with the name does not already exist

        for v in self.value:
            if v.name == val.name:
                self.value.append(val)
                return False
        return True

    def get(self, name):
        """Get index ('address') by name."""
        isPointer = name[0] == "*"
        # if
        value = self.value if type(self.value[0]) is list else [self.value]

        for vi, subvalue in enumerate(value):
            for i, val in enumerate(subvalue):
                if isPointer and val.name == name[1:]:
                    if hasattr(val, "value"):
                        return "-" + str(i)
                if val.name == name:
                    return str(i)
        raise NameError(name, "Not found!")

    def getValue(self):
        """Get value."""
        return self.value

    def getLen(self):
        """Get length of value[]."""
        if type(self.value) is list:
            return len(self.value)
        else:
            return 0

    def getNames(self, listIndex=0):

        return [
            val.getName()
            for val in self.values[listIndex]
        ]
