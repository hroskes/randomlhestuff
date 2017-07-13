#!/usr/bin/env python

import ROOT, rootoverloads, numpy

f = ROOT.TFile("left.root")
tree = f.candTree

def t(i):
  tree.GetEntry(i)
  return tree

M = numpy.matrix([[t(0).left, t(0).right, t(0).int], [t(1).left, t(1).right, t(1).int], [t(2).left, t(2).right, t(2).int]])
b = numpy.matrix([[t(0).L1], [t(1).L1], [t(2).L1]])

coefs = M.I*b
for i in range(20):
  print (numpy.matrix([[t(i).left, t(i).right, t(i).int]])*coefs)[0,0], t(i).L1

c = ROOT.TCanvas()
tree.Draw("{}*left + {}*right + {}*int:L1".format(*coefs.A1.tolist()))
line = ROOT.TLine(0, 0, 1, 1)
line.SetLineColor(ROOT.kRed)
line.Draw()
c.SaveAs("~/www/TEST/test.png")
