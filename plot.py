#!/usr/bin/env python

from math import pi
import ROOT, style, subprocess, sys
import rootoverloads

def plot(cutid=0):

  c = ROOT.TCanvas()

  tleft = ROOT.TChain("candTree")
  tleft.Add("../lhefiles/batch2/left.root")
  tright = ROOT.TChain("candTree")
  tright.Add("../lhefiles/batch2/right.root")
  tSM = ROOT.TChain("candTree")
  tSM.Add("../lhefiles/batch2/SM.root")

  folder = "~/www/TEST/"

  if int(cutid) == 0: cut = "1"
  elif int(cutid) == 1: cut = "D_R>=0.85"; folder += "D_R_big/"
  elif int(cutid) == 2: cut = "D_R<0.85"; folder += "D_R_small/"
  else: assert False, cutid

  cut = "("+cut+")"

  tleft.Draw("1>>normleft"); normleft = ROOT.normleft.Integral()
  tleft.Draw("1>>normleftright", "(right/left)"); normleftright = ROOT.normleftright.Integral()
  tright.Draw("1>>normright"); normright = ROOT.normright.Integral()
  tright.Draw("1>>normrightleft", "(left/right)"); normrightleft = ROOT.normrightleft.Integral()
  tleft.Draw("1>>normmixp", "((left+right+int)/left)"); normmixp = ROOT.normmixp.Integral()
  tleft.Draw("1>>normmixm", "((left+right-int)/left)"); normmixm = ROOT.normmixm.Integral()
  tSM.Draw("1>>normSM"); normSM = ROOT.normSM.Integral()

  discs = "D_LR", "D_L", "D_R", "D_LRint", "costheta1", "costheta2", "costhetastar", "phi", "phi1", "m1", "m2"

  for disc in discs:

    if disc == "D_LRint": continue

    if "cos" in disc: dmin, dmax = -1, 1
    elif "phi" in disc: dmin, dmax = -pi, pi
    elif disc == "m1": dmin, dmax = 0, 100
    elif disc == "m2": dmin, dmax = 0, 100
    else: dmin, dmax = 0, 1

    tleft.Draw(disc+">>hleft"+disc+cutid+"(50,{},{})".format(dmin, dmax), cut)
    hleft = getattr(ROOT, "hleft"+disc+cutid)
    hleft.SetLineColor(2)
    tleft.Draw(disc+">>hleftright"+disc+cutid+"(50,{},{})".format(dmin, dmax), "(right/left)*"+cut)
    hleftright = getattr(ROOT, "hleftright"+disc+cutid)
    hleftright.SetLineColor(7)

    tright.Draw(disc+">>hright"+disc+cutid+"(50,{},{})".format(dmin, dmax), cut)
    hright = getattr(ROOT, "hright"+disc+cutid)
    hright.SetLineColor(4)
    tright.Draw(disc+">>hrightleft"+disc+cutid+"(50,{},{})".format(dmin, dmax), "(left/right)*"+cut)
    hrightleft = getattr(ROOT, "hrightleft"+disc+cutid)
    hrightleft.SetLineColor(6)
    tleft.Draw(disc+">>hmixp"+disc+cutid+"(50,{},{})".format(dmin, dmax), "((left+right+int)/left)*"+cut)
    hmixp = getattr(ROOT, "hmixp"+disc+cutid)
    hmixp.SetLineColor(ROOT.kGreen+3)
    tleft.Draw(disc+">>hmixm"+disc+cutid+"(50,{},{})".format(dmin, dmax), "((left+right-int)/left)*"+cut)
    hmixm = getattr(ROOT, "hmixm"+disc+cutid)
    hmixm.SetLineColor(3)

    tSM.Draw(disc+">>hSM"+disc+cutid+"(50,{},{})".format(dmin, dmax), cut)
    hSM = getattr(ROOT, "hSM"+disc+cutid)
    hSM.SetLineColor(1)

    hstack = ROOT.THStack("hs", "")
    hstack.Add(hSM)
    hstack.Add(hleft)
    hstack.Add(hright)
    hstack.Add(hleftright)
    hstack.Add(hrightleft)
    hstack.Add(hmixp)
    hstack.Add(hmixm)

    histsnorms = (hSM, normSM), (hleft, normleft), (hright, normright), (hleftright, normleftright), (hrightleft, normrightleft), (hmixp, normmixp), (hmixm, normmixm)
    for _ in hstack.GetHists(): assert any(_ is hist for hist, norm in histsnorms)
    for hist, norm in histsnorms: hist.Scale(1./norm)

    l = ROOT.TLegend(.6, .6, .9, .9)
    l.SetFillStyle(0)
    l.SetBorderSize(0)
    l.AddEntry(hSM, "SM", "l")
    l.AddEntry(hleft, "left", "l")
    l.AddEntry(hright, "right", "l")
    l.AddEntry(hleftright, "left rwt to right", "l")
    l.AddEntry(hrightleft, "right rwt to left", "l")
    l.AddEntry(hmixp, "f_{L}=f_{R}=0.5 #phi=0", "l")
    l.AddEntry(hmixm, "f_{L}=f_{R}=0.5 #phi=#pi", "l")

    hstack.Draw("hist nostack")
    hstack.GetXaxis().SetTitle(disc.replace("D_", "D_{").replace("LR", "L/R") + ("}" if "D_" in disc else ""))
    l.Draw()

    exts = "png eps root pdf C"
    print disc
    for ext in exts.split(): c.SaveAs(folder+disc+"."+ext)


  tleft.Draw("D_LRint>>hleftint"+cutid+"(50,-1,1)", cut)
  hleftint = getattr(ROOT, "hleftint"+cutid)
  hleftint.SetLineColor(2)
  tright.Draw("D_LRint>>hrightint"+cutid+"(50,-1,1)", cut)
  hrightint = getattr(ROOT, "hrightint"+cutid)
  hrightint.SetLineColor(4)
  tleft.Draw("D_LRint>>hmixpint"+cutid+"(50,-1,1)", "((left+right+int)/left)*"+cut)
  tleft.Draw("D_LRint>>hmixmint"+cutid+"(50,-1,1)", "((left+right-int)/left)*"+cut)
  hmixpint = getattr(ROOT, "hmixpint"+cutid)
  hmixpint.SetLineColor(ROOT.kGreen+3)
  hmixmint = getattr(ROOT, "hmixmint"+cutid)
  hmixmint.SetLineColor(3)

  hstack = ROOT.THStack("hs2", "")
  hstack.Add(hleftint)
  hstack.Add(hrightint)
  hstack.Add(hmixpint)
  hstack.Add(hmixmint)

  histsnorms = (hleftint, normleft), (hrightint, normright), (hmixpint, normmixp), (hmixmint, normmixm)
  for _ in hstack.GetHists(): assert any(_ is hist for hist, norm in histsnorms)
  for hist, norm in histsnorms: hist.Scale(1./norm)

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

  for ext in exts.split(): c.SaveAs(folder+"D_LRint"+"."+ext)

  tright.Draw("m1:m2>>hm1m2right"+cutid+"(50,0,100,50,0,100)", cut, "COLZ")
  for ext in exts.split(): c.SaveAs(folder+"m12_2d/right."+ext)
  tleft.Draw("m1:m2>>hm1m2left"+cutid+"(50,0,100,50,0,100)", cut, "COLZ")
  for ext in exts.split(): c.SaveAs(folder+"m12_2d/left."+ext)
  tSM.Draw("m1:m2>>hm1m2SM"+cutid+"(50,0,100,50,0,100)", cut, "COLZ")
  for ext in exts.split(): c.SaveAs(folder+"m12_2d/SM."+ext)

if __name__ == "__main__":
  if sys.argv[1:]:
    plot(*sys.argv[1:])
  else:
    plot("0")
    plot("1")
    plot("2")
