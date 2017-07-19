#!/usr/bin/env python

import ROOT, rootoverloads, style

f = ROOT.TFile("../lhefiles/batch2/left.root")
t = f.candTree
c = ROOT.TCanvas()

SM, L, R = (-1.01396946768+0.0551089908689j), (0.541375132608), (-0.465609601233)

fmt = dict(
SMfactor = abs(SM)**2,
Lfactor = L**2,
Rfactor = R**2,
SMLRefactor = SM.real * L,
SMLImfactor = SM.imag * L,
SMRRefactor = SM.real * R,
SMRImfactor = SM.imag * R,
LRfactor = L*R,
)


t.Draw("m1>>htotal(100,0,100)", "fL10p5/left")
htotal = ROOT.htotal

t.Draw("m1>>hSM(100,0,100)", "SM*{SMfactor}/left".format(**fmt))
hSM = ROOT.hSM
hSM.SetLineColor(2)

t.Draw("m1>>hleft(100,0,100)", "left*{Lfactor}/left".format(**fmt))
hleft = ROOT.hleft
hleft.SetLineColor(4)

t.Draw("m1>>hright(100,0,100)", "right*{Rfactor}/left".format(**fmt))
hright = ROOT.hright
hright.SetLineColor(ROOT.kGreen+3)

t.Draw("m1>>hSML(100,0,100)", "SML*{SMLRefactor}/left".format(**fmt))
hSML = ROOT.hSML
hSML.SetLineColor(3)

t.Draw("m1>>hSMR(100,0,100)", "SMR*{SMRRefactor}/left".format(**fmt))
hSMR = ROOT.hSMR
hSMR.SetLineColor(7)

t.Draw("m1>>hSMLim(100,0,100)", "SML_im*{SMLImfactor}/left".format(**fmt))
hSMLim = ROOT.hSMLim
hSMLim.SetLineColor(3)
hSMLim.SetLineStyle(2)

t.Draw("m1>>hSMRim(100,0,100)", "SMR_im*{SMRImfactor}/left".format(**fmt))
hSMRim = ROOT.hSMRim
hSMRim.SetLineColor(7)
hSMRim.SetLineStyle(2)

t.Draw("m1>>hLR(100,0,100)", "LR*{LRfactor}/left".format(**fmt))
hLR = ROOT.hLR
hLR.SetLineColor(6)

hs = ROOT.THStack("hs", "")
hs.Add(htotal)
hs.Add(hSM)
hs.Add(hleft)
hs.Add(hright)
hs.Add(hSML)
hs.Add(hSMLim)
hs.Add(hSMR)
hs.Add(hSMRim)
hs.Add(hLR)

l = ROOT.TLegend(.2, .53, .5, .9)
l.SetBorderSize(0)
l.SetFillStyle(0)

l.AddEntry(htotal, "f_{#Lambda1}=0.5", "l")
l.AddEntry(hSM, "SM", "l")
l.AddEntry(hleft, "L", "l")
l.AddEntry(hright, "R", "l")
l.AddEntry(hSML, "SM-L real int", "l")
l.AddEntry(hSMLim, "SM-L imag int", "l")
l.AddEntry(hSMR, "SM-R real int", "l")
l.AddEntry(hSMRim, "SM-R imag int", "l")
l.AddEntry(hLR, "L-R int", "l")

hs.Draw("hist nostack")
l.Draw()

print htotal.Integral(), sum(_.Integral() for _ in (hSM, hleft, hright, hSML, hSMLim, hSMR, hSMRim, hLR))
print hSMRim.Integral(), hSMLim.Integral()

for ext in "png eps root pdf".split():
  c.SaveAs("~/www/contactterms/newimplementation/flavoruniversal/m1_fL1."+ext)
