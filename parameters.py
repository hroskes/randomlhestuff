#!/usr/bin/env python

from math import sqrt
from functools import wraps
dsqrt = sqrt

import os
import re

def cache(function):
    cache = {}
    @wraps(function)
    def newfunction(*args, **kwargs):
        try:
            return cache[args, tuple(sorted(kwargs.iteritems()))]
        except TypeError:
            print args, tuple(sorted(kwargs.iteritems()))
            raise
        except KeyError:
            cache[args, tuple(sorted(kwargs.iteritems()))] = function(*args, **kwargs)
            return newfunction(*args, **kwargs)
    return newfunction

@cache
def getparameter(name):
  filename = os.path.join(os.path.dirname(__file__), "..", "JHUGen", "JHUGenerator", "mod_Parameters.F90")
  regex = (
           r"^"
           r"\s*"
           r"(?:logical|(?:complex|real)(?:\([\w]*\))?|integer)"
           r"(?:\s*,\s*\w*)*\s*"
           r"::\s*"
           +name.lower()+
           r"[\s!]*=\s*"
           r"([a-z0-9_.+\-*/(), ]*)"
           r"\s*(?:[!].*)?"
           r"$"
          )
  with open(filename) as f:
    for line in f:
      match = re.search(regex, line.lower().strip())
      if match:
        r = match.group(1)
        r = r.replace("_dp", "")
        r = re.sub(r"\b([0-9.]+)d", r"\1e", r)
        rr = r
        gev = 1
        while True:
          match2 = re.search(r"\b[a-z_]\w*\b", rr)
          if not match2: break
          match2 = match2.group(0)
          if match2 not in globals():
            globals()[match2] = getparameter(match2)
          rr = rr.replace(match2, "")
        r = eval(r)
        if isinstance(r, tuple): r = complex(*r)
        return r
  raise IOError("Didn't find {} in mod_Parameters".format(name))

if __name__ == "__main__":
  print getparameter("Brhadr_W_ud")
  print getparameter("pi")
