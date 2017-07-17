#!/usr/bin/env python

import ROOT, rootoverloads, numpy

f = ROOT.TFile("../lhefiles/batch2/left_Z.root")
tree = f.candTree

def t(i):
  tree.GetEntry(i)
  return tree

probs = ["left", "right", "LR", "SM", "SML", "SMR"]

c = ROOT.TCanvas()

def draw(target, saveas):
  M = numpy.matrix([[getattr(t(i), prob) for prob in probs] for i, _ in enumerate(probs)])
  b = numpy.matrix([[getattr(t(i), target)] for i, _ in enumerate(probs)])

  coefs = M.I*b
  for i in range(20):
    print (numpy.matrix([[getattr(t(i), prob) for prob in probs]])*coefs)[0,0], getattr(t(i), target)

  print probs
  print coefs

  tree.Draw("+".join("{}*{}".format(coef, prob) for coef, prob in zip(numpy.array(coefs).flatten().tolist(), probs)) + ":" + target)
  line = ROOT.TLine(0, 0, 1, 1)
  line.SetLineColor(ROOT.kRed)
  line.Draw()
  c.SaveAs("~/www/contactterms/newimplementation/flavoruniversal/{}.png".format(saveas))

draw("L1", "L1linearcombination_withSM")
draw("L1Zg", "L1Zglinearcombination_withSM")
draw("fa1fL1fL1Zg0p33", "a1L1L1Zglinearcombination")
