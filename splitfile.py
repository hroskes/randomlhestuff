import os
from enum import MyEnum, EnumItem
from frozencounter import FrozenCounter

class Particle(MyEnum):
    enumitems = (
                 EnumItem("e", 11, -11),
                 EnumItem("mu", 13, -13),
                 EnumItem("tau", 15, -15),
                 EnumItem("q", 1, 2, 3, 4, 5, -1, -2, -3, -4, -5),
                )

class ParticleCounter(FrozenCounter):
    def __init__(self, *args):
        return FrozenCounter.__init__(self, (Particle(p) for p in args))

class DecayMode(MyEnum):
    enumitems = (
                 EnumItem("2e2mu", 0, ParticleCounter(11, -11, 13, -13)),
                 EnumItem("4e", 1, ParticleCounter(11, -11, 11, -11)),
                 EnumItem("4mu", 2, ParticleCounter(13, -13, 13, -13)),
                 EnumItem("2e2tau", 3, ParticleCounter(11, -11, 15, -15)),
                 EnumItem("2mu2tau", 4, ParticleCounter(13, -13, 15, -15)),
                 EnumItem("4tau", 5, ParticleCounter(15, -15, 15, -15)),
                 EnumItem("2l2q", 6, *(ParticleCounter(l, l, "q", "q") for l in ("e", "mu", "tau"))),
                 EnumItem("4q", 7, ParticleCounter("q", "q", "q", "q")),
                )

decaymodes = [DecayMode(a) for a in DecayMode.enumitems]

def splitfile(*files):
    for filename in files:
        linenumber = 0
        with open(filename) as f:
            newfs = {}
            for decaymode in decaymodes:
                newfilename = filename.replace(".lhe", "_%s.lhe" % decaymode)
                #if os.path.exists(newfilename):
                #    raise ValueError("%s already exists!" % newfilename)
                newfs[decaymode] = open(newfilename, "w")

            thisevent = ""
            header = True
            inevent = False
            lineinevent = -2
            Higgs = None
            Zs = set()
            Hdecaylist = []
            for line in f:
                if "<event>" in line:
                    for decaymode, newf in newfs.iteritems():
                        newf.write(thisevent)
                    thisevent = ""
                    header = False
                    inevent = True
                    del Hdecaylist[:]
                    lineinevent = -2 #-1 is <event>, 0 is initline, 1 is first particle
                    electrons = 0
                    muons = 0

                if inevent:
                    data = line.split()

                thisevent += line
                lineinevent += 1
                linenumber += 1

                if "</event>" in line:
                    inevent = False
                    particles = ParticleCounter(*Hdecaylist)
                    try:
                        newfs[DecayMode(particles)].write(thisevent)
                    except KeyError:
                        raise KeyError("Unknown event! %i" % linenumber)
                    thisevent = ""

                if inevent:
                    try:
                        id = int(data[0])
                        mother = int(data[2])
                        if id in (25, 32, 39):
                            if Higgs is None:
                                Higgs = lineinevent
                            else:
                                raise ValueError
                        elif mother == Higgs:
                            Zs.add(lineinevent)
                        elif mother in Zs:
                            Hdecaylist.append(id)
                    except (ValueError, KeyError):
                        pass

            for decaymode, newf in newfs.iteritems():
                newf.write(thisevent)

if __name__ == "__main__":
    import sys
    splitfile(*sys.argv[1:])
