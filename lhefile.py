import abc

import ROOT

from mela import Mela, SimpleParticleCollection_t

class LHEFileBase(object):
    __metaclass__ = abc.ABCMeta

    """
    Simple class to iterate through an LHE file and calculate probabilities for each event
    Example usage:
    h1 = ROOT.TH1F("costheta1", "costheta1", 100, -1, 1)
    h2 = ROOT.TH1F("D_0minus", "D_0minus", 100, 0, 1)
    with LHEFile("filename.lhe") as f:
        for event in f:  #event becomes the mela object
            h1.Fill(event.computeDecayAngles().costheta1)
            event.ghz1 = 1
            p0plus = event.computeP()
            event.ghz4 = 1
            p0minus = event.computeP()
            h2.Fill(p0plus / (p0plus + p0minus))
    """
    def __init__(self, filename, *melaargs, **kwargs):
        self.isgen = kwargs.pop("isgen", True)
        if kwargs: raise ValueError("Unknown kwargs: " + ", ".join(kwargs))
        self.filename = filename
        self.mela = Mela(*melaargs)
        self.f = open(self.filename)
    def __enter__(self, *args, **kwargs):
        self.f.__enter__(*args, **kwargs)
        return self
    def __exit__(self, *args, **kwargs):
        return self.f.__exit__(*args, **kwargs)

    def __iter__(self):
        event = ""
        for linenumber, line in enumerate(self.f, start=1):
            if "<event>" not in line and not event:
                continue
            event += line
            if "</event>" in line:
                try:
                    self._setInputEvent(event)
                    yield self.mela
                    event = ""
                except GeneratorExit:
                    raise
                except:
                    print "On line", linenumber
                    raise
                finally:
                    try:
                        self.mela.resetInputEvent()
                    except:
                        pass

    @abc.abstractmethod
    def _setInputEvent(self, event): pass

    @classmethod
    def _LHEclassattributes(cls):
        return "filename", "f", "mela"

    def __getattr__(self, attr):
        return getattr(self.mela, attr)
    def __setattr__(self, attr, value):
        if attr in self._LHEclassattributes():
            super(LHEFile_JHUGenVBFVH, self).__setattr__(attr, value)
        else:
            setattr(self.mela, attr, value)

class LHEFile_Hwithdecay(object):
    def _setInputEvent(self, event):
        self.mela.setInputEvent_fromLHE(event, self.isgen)
        

class LHEFile_JHUGenVBFVH(object):
    def _setInputEvent(self, event):
        particles = event.strip().split("\n")[2:-1]  #remove the first 2 lines, <event> and event info, and the last line, </event>
        self.daughters = SimpleParticleCollection_t([particle for particle in particles if int(particle.split()[0]) == 25])
        self.associated = SimpleParticleCollection_t([particle for particle in particles
                                                       if abs(int(particle.split()[0])) in (1, 2, 3, 4, 5, 11, 12, 13, 14, 15, 16)
                                                       and int(particle.split()[1]) == 1])
        self.mothers = SimpleParticleCollection_t([particle for particle in particles if int(particle.split()[1]) == -1])
        assert len(self.daughters) == 1 and len(self.associated) == len(self.mothers) == 2
        self.mela.setInputEvent(self.daughters, self.associated, self.mothers, True)
    @classmethod
    def _LHEclassattributes(cls):
        return super(cls).LHEclassattributes() + ("daughters", "mothers", "associated")
