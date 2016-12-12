#!/usr/bin/env python

from collections import namedtuple
from lhefile import LHEFile
from math import pi
import os
import ROOT
from ZZMatrixElement.PythonWrapper.mela import Mela

DecayAngles = Mela.DecayAngles

class M4lRange(namedtuple("M4lRange", "low hi")):
  def __contains__(self, other):
    return self.low <= other <= self.hi

plotsbasedir = "plots"
exts = "png eps root pdf".split()

def plots(filenames, m4lranges):
  m4lranges = [M4lRange(*_) for _ in m4lranges]
  bins = 100
  titles = DecayAngles(qH="m_{4l}", m1="m_{Z1}", m2="m_{Z2}", costhetastar="cos#theta*", costheta1="cos#theta_{1}", costheta2="cos#theta_{2}", Phi="#Phi", Phi1="#Phi_{1}")
  mins = DecayAngles(qH=0, m1=40, m2=0, costhetastar=-1, costheta1=-1, costheta2=-1, Phi=-pi, Phi1=-pi)
  maxes = DecayAngles(qH=2000, m1=120, m2=60, costhetastar=1, costheta1=1, costheta2=1, Phi=pi, Phi1=pi)

  hists = {
           _:
              DecayAngles(
                          *(
                            ROOT.TH1F("{}{}{}".format(name, _.low, _.hi), title, bins, min, max)
                               for name, title, min, max in zip(DecayAngles._fields, titles, mins, maxes)
                           )
                         ) for _ in m4lranges
          }

  for color, (m4lrange, histset) in enumerate(hists.iteritems()):
    for h in histset:
      h.SetLineColor(color)

  hstacks = DecayAngles(*(ROOT.THStack(name, title) for name, title in zip(DecayAngles._fields, titles)))

  for filename in filenames:
    with LHEFile(filename) as f:
      print filename
      for i, event in enumerate(f, start=1):
        decayangles = event.computeDecayAngles()
        for m4lrange in m4lranges:
          if decayangles.qH in m4lrange:
            for hist, value in zip(hists[m4lrange], decayangles):
              hist.Fill(value)
        if i % 100 == 0:
          print "Processed", i, "events"
    if i % 100 != 0:
      print "Processed", i, "events"
    break

  for m4lrange in m4lranges:
    for hist, hstack in zip(hists[m4lrange], hstacks):
      hstack.Add(hist)

  legend = ROOT.TLegend(.6, .7, .9, .9)
  for m4lrange in m4lranges:
    legend.AddEntry(hists[m4lrange][0], "{} GeV < m_{{4l}} < {} GeV".format(*m4lrange), "lpf")

  c = ROOT.TCanvas()
  for hstack, name in zip(hstacks, DecayAngles._fields):
    hstack.Draw("hist nostack")
    legend.Draw()
    for ext in exts:
      c.SaveAs(os.path.join(plotsbasedir, "{}.{}".format(name, ext)))

if __name__ == "__main__":
  directory = "/work-zfs/lhc/meng/highmass/MCFM-7.0.2_wBW3456_BASE_0+m_PRODUCTIONREADY_SM2/Bin/m450d0VBF_BSI_QCD247_ELMU"
  plots((os.path.join(directory, _) for _ in os.listdir(directory) if _.endswith(".lhe")), [(89.2, 93.2), (170, 190)])
