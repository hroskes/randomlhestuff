class Event(object):
    def __init__(self, eventstr):
        self.eventstr = eventstr
        lines = (line for line in eventstr.split("\n") if line and "event>" not in line)
        next(lines) #skip nparticles
        t = b = None
        for line in lines:
             id = int(line.split()[0])
             mothers = [int(_) for _ in line.split()[2:4]]
             if abs(id) == 6:
                 assert not t
                 t = line
                 colors = [int(_) for _ in line.split()[4:6]]
                 if id == 6 and colors[0] == 501:
                     self.process = 110
                 elif id == -6 and colors[1] == 501:
                     self.process = 111
                 elif id == 6 and colors[0] == 502:
                     self.process = 112
                 elif id == -6 and colors[1] == 502:
                     self.process = 113
                 else:
                     assert False
             if abs(id) == 5 and mothers != [4, 4] and mothers != [7, 7]:
                 assert not b
                 b = line

        assert t
        assert b

        bid, bstatus, bcolors = int(b.split()[0]), int(b.split()[1]), [int(_) for _ in b.split()[4:6]]

        if self.process == 110: assert bid ==  5 and bstatus == -1 and bcolors == [501, 0]
        if self.process == 111: assert bid == -5 and bstatus == -1 and bcolors == [0, 501]
        if self.process == 112: assert bid == -5 and bstatus ==  1 and bcolors == [0, 502]
        if self.process == 113: assert bid ==  5 and bstatus ==  1 and bcolors == [502, 0]

class LHEFile(object):
    def __init__(self, filename):
        self.filename = filename
    def __enter__(self, *args, **kwargs):
        self.f = open(self.filename)
        self.f.__enter__(*args, **kwargs)
        return self
    def __exit__(self, *args, **kwargs):
        self.f.__exit__(*args, **kwargs)

    def __iter__(self):
        event = ""
        for linenumber, line in enumerate(self.f, start=1):
            if "<event>" not in line and not event:
                continue
            event += line
            if "</event>" in line:
                try:
                    yield Event(event)
                    event = ""
                except:
                    print "On line", linenumber
                    raise

lheheader = """<LesHouchesEvents version="1.0">
<!--
Process=114, filtered for Process={process}
-->
<init>
2212 2212   6500.0000000000000000    6500.0000000000000000 0 0   10042   10042  3  1
 1.  1.  1.0000000E+00 {process}
</init>
"""
lhefooter = """</LesHouchesEvents>"""


def split(filename):
    newf = {}
    with LHEFile(filename) as f, open("110.lhe", "w") as newf[110], open("111.lhe", "w") as newf[111], open("112.lhe", "w") as newf[112], open("113.lhe", "w") as newf[113]:
        for k, v in newf.iteritems():
             v.write(lheheader.format(process=k))
        for event in f:
             newf[event.process].write(event.eventstr)
        for k, v in newf.iteritems():
             v.write(lhefooter)

if __name__ == "__main__":
    split("114.lhe")
