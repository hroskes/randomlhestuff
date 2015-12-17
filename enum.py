class EnumItem(object):
    def __init__(self, name, code, *other):
        self.name = name
        self.code = code
        self.names = tuple([name, code] + list(other))

    def __str__(self):
        return self.name
    def __int__(self):
        return self.code
    def __format__(self, format_spec):
        return format(int(self), format_spec)
    def __hash__(self):
        return hash(self.names)

    def __eq__(self, other):
        if type(other) == int or type(other) == str:
            return other in self.names
        return str(self) == str(other) and int(self) == int(other)
    def __ne__(self, other):
        return not self == other

class MyEnum(object):
    def __init__(self, value):
        if isinstance(value, (MyEnum, EnumItem)):
            value = str(value)
        for item in self.enumitems:
            if value in item.names:
                self.item = item
                break
        else:
            raise ValueError(str(value) + " is not a member of enum " + type(self).__name__ + "!  Valid choices:\n"
                               + "\n".join(" aka ".join(str(name) for name in item.names) for item in self.enumitems))

    def __str__(self):
        return str(self.item)
    def __repr__(self):
        return type(self).__name__ + "(" + repr(str(self.item)) + ")"
    def __int__(self):
        return int(self.item)
    def __format__(self, format_spec):
        return format(self.item, format_spec)

    def __eq__(self, other):
        try:
            return self.item == other.item
        except AttributeError:
            return self.item == other
    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.item)
