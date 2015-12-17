from collections import Mapping, Counter

class FrozenCounter(Mapping, Counter):
    def __init__(self, iterable):
        self.__finishedinit = False
        Counter.__init__(self, iterable)
        self.__finishedinit = True
    def __getitem__(self, key):
        return Counter.__getitem__(self, key)
    def __iter__(self):
        return Counter.__iter__(self)
    def __len__(self):
        return Counter.__len__(self)
    def __hash__(self):
        return hash(frozenset(self.iteritems()))
    def __setitem__(self, *args, **kwargs):
        if self.__finishedinit:
            raise AttributeError("Can't change a frozen counter!")
        Counter.__setitem__(self, *args, **kwargs)
    def __delitem__(self, *args, **kwargs):
        if self.__finishedinit:
            raise AttributeError("Can't change a frozen counter!")
        Counter.__delitem__(self, *args, **kwargs)
    def clear(self, *args, **kwargs):
        raise AttributeError("Can't change a frozen counter!")
    def pop(self, *args, **kwargs):
        raise AttributeError("Can't change a frozen counter!")
    def popitem(self, *args, **kwargs):
        raise AttributeError("Can't change a frozen counter!")
