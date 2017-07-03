#!/usr/bin/env python

import ROOT, style, subprocess

c = ROOT.TCanvas()

tleft = ROOT.TChain("candTree")
tleft.Add("../JHUGen/JHUGenerator/left.root")
tleft.Draw("D_LR_E>>hleft(100,0,1)")
hleft = ROOT.hleft
hleft.SetLineColor(2)
tleft.Draw("D_LR_E>>hleftright(100,0,1)", "right/left")
hleftright = ROOT.hleftright
hleftright.SetLineColor(7)

tright = ROOT.TChain("candTree")
tright.Add("../JHUGen/JHUGenerator/right.root")
tright.Draw("D_LR_E>>hright(100,0,1)")
hright = ROOT.hright
hright.SetLineColor(4)
tright.Draw("D_LR_E>>hrightleft(100,0,1)", "left/right")
hrightleft = ROOT.hrightleft
hrightleft.SetLineColor(6)
tleft.Draw("D_LR_E>>hmixp(100,0,1)", "(left+right+int)/left")
hmixp = ROOT.hmixp
hmixp.SetLineColor(ROOT.kGreen+3)

hstack = ROOT.THStack("hs", "")
hstack.Add(hleft)
hstack.Add(hright)
hstack.Add(hleftright)
hstack.Add(hrightleft)
hstack.Add(hmixp)

for _ in hstack.GetHists(): _.Scale(1/_.Integral())

l = ROOT.TLegend(.6, .6, .9, .9)
l.SetFillStyle(0)
l.SetBorderSize(0)
l.AddEntry(hleft, "left", "l")
l.AddEntry(hright, "right", "l")
l.AddEntry(hleftright, "left rwt to right", "l")
l.AddEntry(hrightleft, "right rwt to left", "l")
l.AddEntry(hmixp, "mix #phi=0", "l")

hstack.Draw("hist nostack")
hstack.GetXaxis().SetTitle("D_{L/R}")
l.Draw()

exts = "png eps root pdf C"
for ext in exts.split(): c.SaveAs("D_LR."+ext)


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

for ext in exts.split(): c.SaveAs("D_LRint."+ext)

subprocess.check_call(["rsync", "-azvI"] + ["D_"+disc+"."+ext for ext in exts.split() for disc in ("LR", "LRint")] + ["hroskes@lxplus.cern.ch:www/contactterms"])
