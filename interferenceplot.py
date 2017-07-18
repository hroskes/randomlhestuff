#!/usr/bin/env python

import ROOT, rootoverloads

f = ROOT.TFile("../lhefiles/batch2/left.root")
c = ROOT.TCanvas()

t.Draw("m1>>htotal(100,0,100)", "fL10p5/left")
htotal = ROOT.htotal

t.Draw("m1>>hSM(100,0,100)", "SM*{SMfactor}*{SMfactor}/left".format(**fmt))
hSM = ROOT.hSM

t.Draw("m1>>hleft(100,0,100)", "left*{leftfactor}*{leftfactor}/left".format(**fmt))
hleft = ROOT.hleft

t.Draw("m1>>hright(100,0,100)", "right*{rightfactor}*{rightfactor}/right".format(**fmt))
hright = ROOT.hright

t.Draw("m1>>hSML(100,0,100)", "(SML*{SMRefactor} + SML_im*{SMImfactor})*{leftfactor}/left".format(**fmt))
hSM = ROOT.hSML

t.Draw("m1>>hSMR(100,0,100)", "SMR*{SMfactor}*{rightfactor}/right".format(**fmt))
hSM = ROOT.hSMR

t.Draw("m1>>hLR(100,0,100)", "LR*{leftfactor}*{rightfactor}/right".format(**fmt))
hL = ROOT.hLR

hstack = ROOT.THStack("hs", "")
