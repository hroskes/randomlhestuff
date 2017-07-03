import ROOT
from mela import Mela

class LHEFile(object):
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
    mela = {}
    def __init__(self, filename, *melaargs):
        self.filename = filename
        if melaargs not in LHEFile.mela:
            LHEFile.mela[melaargs] = Mela(*melaargs)
        self.mela = LHEFile.mela[melaargs]
        self.f = open(self.filename)
        #for event in self: break #initialize mass and xsec
    def __enter__(self, *args, **kwargs):
        self.f.__enter__(*args, **kwargs)
        return self
    def __exit__(self, *args, **kwargs):
        return self.f.__exit__(*args, **kwargs)

    @property
    def mass(self):
        if "1TeV" in self.filename: return 1000
        else: return 125

    def __iter__(self):
        event = ""
        for linenumber, line in enumerate(self.f, start=1):
            if "<event>" not in line and not event:
                continue
            event += line
            if "</event>" in line:
                try:
                    self.mela.setInputEvent_fromLHE(event, True)
                    yield self.mela
                    event = ""
                except:
                    print "On line", linenumber
                    raise
                finally:
                    try:
                        self.mela.resetInputEvent()
                    except:
                        pass
