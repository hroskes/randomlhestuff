#!/usr/bin/env python

from math import pi
import ROOT, style, subprocess, sys

def plot(mreso):

  c = ROOT.TCanvas()

  tleft = ROOT.TChain("candTree")
  tleft.Add("../JHUGen/JHUGenerator/left"+mreso+".root")
  tright = ROOT.TChain("candTree")
  tright.Add("../JHUGen/JHUGenerator/right"+mreso+".root")
  tSM = ROOT.TChain("candTree")
  tSM.Add("../JHUGen/JHUGenerator/SM"+mreso+".root")

  discs = "D_LR_E", "D_L_E", "D_R_E", "D_LRint_E", "costheta1", "costheta2", "costhetastar", "phi", "phi1", "m1", "m2"

  for disc in discs:

    if disc == "D_LRint_E": continue

    if "cos" in disc: dmin, dmax = -1, 1
    elif "phi" in disc: dmin, dmax = -pi, pi
    elif disc == "m1": dmin, dmax = 0, 100
    elif disc == "m2": dmin, dmax = 0, 100
    else: dmin, dmax = 0, 1

    tleft.Draw(disc+">>hleft"+disc+"(100,{},{})".format(dmin, dmax))
    hleft = getattr(ROOT, "hleft"+disc)
    hleft.SetLineColor(2)
    tleft.Draw(disc+">>hleftright"+disc+"(100,{},{})".format(dmin, dmax), "right/left")
    hleftright = getattr(ROOT, "hleftright"+disc)
    hleftright.SetLineColor(7)

    tright.Draw(disc+">>hright"+disc+"(100,{},{})".format(dmin, dmax))
    hright = getattr(ROOT, "hright"+disc)
    hright.SetLineColor(4)
    tright.Draw(disc+">>hrightleft"+disc+"(100,{},{})".format(dmin, dmax), "left/right")
    hrightleft = getattr(ROOT, "hrightleft"+disc)
    hrightleft.SetLineColor(6)
    tleft.Draw(disc+">>hmixp"+disc+"(100,{},{})".format(dmin, dmax), "(left+right+int)/left")
    hmixp = getattr(ROOT, "hmixp"+disc)
    hmixp.SetLineColor(ROOT.kGreen+3)

    tSM.Draw(disc+">>hSM"+disc+"(100,{},{})".format(dmin, dmax))
    hSM = getattr(ROOT, "hSM"+disc)
    hSM.SetLineColor(1)

    hstack = ROOT.THStack("hs", "")
    hstack.Add(hSM)
    hstack.Add(hleft)
    hstack.Add(hright)
    hstack.Add(hleftright)
    hstack.Add(hrightleft)
    hstack.Add(hmixp)

    for _ in hstack.GetHists(): _.Scale(1/_.Integral())

    l = ROOT.TLegend(.6, .6, .9, .9)
    l.SetFillStyle(0)
    l.SetBorderSize(0)
    l.AddEntry(hSM, "SM", "l")
    l.AddEntry(hleft, "left", "l")
    l.AddEntry(hright, "right", "l")
    l.AddEntry(hleftright, "left rwt to right", "l")
    l.AddEntry(hrightleft, "right rwt to left", "l")
    l.AddEntry(hmixp, "f_{L}=f_{R}=0.5 #phi=0", "l")

    hstack.Draw("hist nostack")
    hstack.GetXaxis().SetTitle(disc.replace("_E", "}").replace("D_", "D_{").replace("LR", "L/R"))
    l.Draw()

    exts = "png eps root pdf C"
    print disc
    for ext in exts.split(): c.SaveAs(disc.replace("_E", "")+mreso+"."+ext)


  tleft.Draw("D_LRint_E>>hleftint(100,-1.5e-7,1.5e-7)")
  hleftint = ROOT.hleftint
  hleftint.SetLineColor(2)
  tright.Draw("D_LRint_E>>hrightint(100,-1.5e-7,1.5e-7)")
  hrightint = ROOT.hrightint
  hrightint.SetLineColor(4)
  tleft.Draw("D_LRint_E>>hmixpint(100,-1.5e-7,1.5e-7)", "(left+right+int)/left")
  tleft.Draw("D_LRint_E>>hmixmint(100,-1.5e-7,1.5e-7)", "(left+right-int)/left")
  hmixpint = ROOT.hmixpint
  hmixpint.SetLineColor(ROOT.kGreen+3)
  hmixmint = ROOT.hmixmint
  hmixmint.SetLineColor(1)

  hstack = ROOT.THStack("hs2", "")
  hstack.Add(hleftint)
  hstack.Add(hrightint)
  hstack.Add(hmixpint)
  hstack.Add(hmixmint)

  for _ in hstack.GetHists(): _.Scale(1/_.Integral())

  l = ROOT.TLegend(.6, .6, .9, .9)
  l.SetFillStyle(0)
  l.SetBorderSize(0)
  l.AddEntry(hleft, "left", "l")
  l.AddEntry(hright, "right", "l")
  l.AddEntry(hmixpint, "mix #phi=0", "l")
  l.AddEntry(hmixmint, "mix #phi=#pi", "l")

  hstack.Draw("hist nostack")
  hstack.GetXaxis().SetTitle("D_{int}^{L/R}")
  l.Draw()

  for ext in exts.split(): c.SaveAs("D_LRint"+mreso+"."+ext)

  folder = "1TeV" if mreso == "_1TeV" else "125GeV"
  subprocess.check_call(["rsync", "-azvI"] + [disc.replace("_E", "")+mreso+"."+ext for ext in exts.split() for disc in discs] + ["hroskes@lxplus.cern.ch:www/contactterms/"+folder])

if __name__ == "__main__":
  if sys.argv[1:]:
    plot(*sys.argv[1:])
  else:
    plot("")
