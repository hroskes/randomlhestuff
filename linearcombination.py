#!/usr/bin/env python

import ROOT, rootoverloads, numpy

f = ROOT.TFile("../lhefiles/batch2/left.root")
tree = f.candTree

def t(i):
  tree.GetEntry(i)
  return tree

probs = ["left", "right", "int"]

M = numpy.matrix([[getattr(t(i), prob) for prob in probs] for i, _ in enumerate(probs)])
b = numpy.matrix([[t(i).L1] for i, _ in enumerate(probs)])

coefs = M.I*b
for i in range(20):
  print (numpy.matrix([[getattr(t(i), prob) for prob in probs]])*coefs)[0,0], t(i).L1

c = ROOT.TCanvas()
tree.Draw("+".join("{}*{}".format(coef, prob) for coef, prob in zip(numpy.array(coefs).flatten().tolist(), probs)) + ":L1")
line = ROOT.TLine(0, 0, 1, 1)
line.SetLineColor(ROOT.kRed)
line.Draw()
c.SaveAs("~/www/TEST/test.png")
