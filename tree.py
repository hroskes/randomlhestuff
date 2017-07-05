#!/usr/bin/env python

from array import array
from math import pi, sqrt
import os
import sys

import ROOT

from lhefile import LHEFile
from mela import TVar
from parameters import getparameter

#working from griffiths 2nd edition page 331-332
#and andrei's email "more on PO"
e = 1  #overall factor doesn't matter until we want interference between SM and contact terms
ge = e*sqrt(4*pi)
sinthetaW = sqrt(getparameter("xw"))
costhetaW = sqrt(1-sinthetaW**2)
gZ = ge / (sinthetaW*costhetaW)
cVe = -.5 + 2*sinthetaW**2
cAe = -.5
gZeL = gZ*(cVe+cAe)
gZeR = gZ*(cVe-cAe)
M_Z = getparameter("M_Z")
vev = getparameter("vev")
Lambda_1 = getparameter("Lambda_1")
Lambda_zgs1 = getparameter("Lambda_zgs1")

def lhe2tree(filename):
  newfilename = filename.replace(".lhe", ".root")
  assert os.path.exists(filename)
  f = ROOT.TFile(newfilename, "CREATE")
  if not f.IsWritable(): return
  t = ROOT.TTree("candTree", "")
  bad = False
  try:
    left = array('d', [0])
    right = array('d', [0])
    int = array('d', [0])
    SM = array('d', [0])
    L1 = array('d', [0])
    L1Zg = array('d', [0])
    L1_contact = array('d', [0])
    L1Zg_contact = array('d', [0])
    D_L_E = array('d', [0])
    D_R_E = array('d', [0])
    D_LR_E = array('d', [0])
    D_LRint_E = array('d', [0])
    t.Branch("left", left, "left/D")
    t.Branch("right", right, "right/D")
    t.Branch("SM", SM, "SM/D")
    t.Branch("int", int, "int/D")
    t.Branch("L1", L1, "L1/D")
    t.Branch("L1Zg", L1Zg, "L1Zg/D")
    t.Branch("L1_contact", L1_contact, "L1_contact/D")
    t.Branch("L1Zg_contact", L1Zg_contact, "L1Zg_contact/D")
    t.Branch("D_L_E", D_L_E, "D_L_E/D")
    t.Branch("D_R_E", D_R_E, "D_R_E/D")
    t.Branch("D_LR_E", D_LR_E, "D_LR_E/D")
    t.Branch("D_LRint_E", D_LRint_E, "D_LRint_E/D")

    with LHEFile(filename) as lhe:

      if lhe.mass == 125:
        leftxsec = 3.2287305
        rightxsec = 3.2270333
        SMxsec = 1.4604303E+01
      elif lhe.mass == 1000:
        leftxsec = 6.0604581E+02
        rightxsec = 6.0095973E+02
        SMxsec = 7.2953822E+04

      print filename
      for i, event in enumerate(lhe, start=1):
        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghz1 = event.ehz_L_E = event.OnlyVVpr = 1
        left[0] = event.computeP()
        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghz1 = event.ehz_R_E = event.OnlyVVpr = 1
        right[0] = event.computeP()
        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghz1 = event.ehz_R_E = event.ehz_L_E = event.OnlyVVpr = 1
        int[0] = event.computeP() - left[0] - right[0]
        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghz1 = 1
        SM[0] = event.computeP()

        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghz1_prime2 = 1
        L1[0] = event.computeP()
        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghzgs1_prime2 = 1
        L1Zg[0] = event.computeP()

        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghz1 = 1
        event.ehz_R_E = -gZeR * vev * M_Z**2 / (2 * Lambda_1**2)
        event.ehz_L_E = -gZeL * vev * M_Z**2 / (2 * Lambda_1**2)
        L1_contact[0] = event.computeP()

        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghz1 = 1
        event.ehz_R_E = e * vev * M_Z**2 / (2 * Lambda_zgs1**2)
        event.ehz_L_E = e * vev * M_Z**2 / (2 * Lambda_zgs1**2)
        L1Zg_contact[0] = event.computeP()

        left[0] /= leftxsec
        right[0] /= rightxsec
        int[0] /= sqrt(leftxsec*rightxsec)
        SM[0] /= SMxsec

        D_L_E[0] = left[0] / (left[0] + SM[0])
        D_R_E[0] = right[0] / (right[0] + SM[0])
        D_LR_E[0] = left[0] / (left[0] + right[0])
        D_LRint_E[0] = int[0] / (left[0] + right[0])

        t.Fill()

        if i % 1000 == 0:
          print "processed", i, "events"
  except:
    bad = True
    raise
  finally:
    f.cd()
    t.Write()
    f.Close()
    if bad:
      os.remove(newfilename)

if __name__ == "__main__":
  for _ in sys.argv[1:]:
    lhe2tree(_)
