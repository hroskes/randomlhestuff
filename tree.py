#!/usr/bin/env python

from array import array
from math import pi, sqrt
import os
import sys

import numpy
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
Lambda_z1 = getparameter("Lambda_z1")
Lambda_zgs1 = getparameter("Lambda_zgs1")

#[kappaZZ, eZeR, eZeL]^T = matrix * [a1, g1prime2, ghzgs1prime2]^T
matrix = numpy.matrix(
  [
   [1, 2*M_Z**2 / Lambda_z1**2, 0],
   [0, -gZeR*M_Z**2 / Lambda_z1**2, e*M_Z**2 / Lambda_zgs1**2],
   [0, -gZeL*M_Z**2 / Lambda_z1**2, e*M_Z**2 / Lambda_zgs1**2],
  ]
)
invertedmatrix = matrix.I

a1forleft, g1prime2forleft, ghzgs1prime2forleft = invertedmatrix*numpy.matrix([[0], [0], [1]]).tolist()
a1forright, g1prime2forright, ghzgs1prime2forright = invertedmatrix*numpy.matrix([[0], [1], [0]]).tolist()

def Branch(t, name):
    a = array('d', [0])
    t.Branch(name, a, name+"/D")
    return a

def lhe2tree(filename):
  newfilename = filename.replace(".lhe", ".root")
  assert os.path.exists(filename)
  f = ROOT.TFile(newfilename, "CREATE")
  if not f.IsWritable(): return
  t = ROOT.TTree("candTree", "")
  bad = False
  try:
    costhetastar = Branch(t, "costhetastar")
    costheta1 = Branch(t, "costheta1")
    costheta2 = Branch(t, "costheta2")
    phi = Branch(t, "phi")
    phi1 = Branch(t, "phi1")
    m1 = Branch(t, "m1")
    m2 = Branch(t, "m2")
    m4l = Branch(t, "m4l")

    left = Branch(t, "left")
    right = Branch(t, "right")
    SM = Branch(t, "SM")
    LR = Branch(t, "LR")
    LR_im = Branch(t, "LR_im")
    SML = Branch(t, "SML")
    SML_im = Branch(t, "SML_im")
    SMR = Branch(t, "SMR")
    SMR_im = Branch(t, "SMR_im")
    L1 = Branch(t, "L1")
    L1Zg = Branch(t, "L1Zg")

    D_L = Branch(t, "D_L")
    D_R = Branch(t, "D_R")
    D_LR = Branch(t, "D_LR")
    D_LRint = Branch(t, "D_LRint")

    fa1fL1fL1Zg0p33 = Branch(t, "fa1fL1fL1Zg0p33")
    fa1fL1fL1Zg0p33_positive = Branch(t, "fa1fL1fL1Zg0p33_positive")
    fa1fL1fL1Zg0p33_negative = Branch(t, "fa1fL1fL1Zg0p33_negative")

    with LHEFile(filename) as lhe:

      if lhe.mass == 125:
        leftxsec = 1.4347981E+01
        rightxsec = 1.3952140E+01
        SMxsec = 1.4604303E+01
        L1xsec = 9.955957800124091e-08
        L1Zgxsec = 2.5195854694239526e-07
      elif lhe.mass == 1000:
        leftxsec = 6.0604581E+02
        rightxsec = 6.0095973E+02
        SMxsec = 7.2953822E+04
        L1xsec = L1Zgxsec = 1

      print filename
      for i, event in enumerate(lhe, start=1):
        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghzzp1 = event.ezp_L_E = event.ezp_L_M = event.ezp_L_T = 1
        left[0] = event.computeP()

        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghzzp1 = event.ezp_R_E = event.ezp_R_M = event.ezp_R_T = 1
        right[0] = event.computeP()

        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghzzp1 = event.ezp_R_E = event.ezp_R_M = event.ezp_R_T = event.ezp_L_E = event.ezp_L_M = event.ezp_L_T = 1
        LR[0] = event.computeP() - left[0] - right[0]
        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghzzp1 = event.ezp_R_E = event.ezp_R_M = event.ezp_R_T = 1
        event.ezp_L_E = event.ezp_L_M = event.ezp_L_T = 1j
        LR_im[0] = event.computeP() - left[0] - right[0]

        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghz1 = 1
        SM[0] = event.computeP()

        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghz1 = event.ghzzp1 = event.ezp_L_E = event.ezp_L_M = event.ezp_L_T = 1
        SML[0] = event.computeP() - SM[0] - left[0]
        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghz1 = event.ezp_L_E = event.ezp_L_M = event.ezp_L_T = 1
        event.ghzzp1 = 1j
        SML_im[0] = event.computeP() - SM[0] - left[0]

        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghz1 = event.ghzzp1 = event.ezp_R_E = event.ezp_R_M = event.ezp_R_T = 1
        SMR[0] = event.computeP() - SM[0] - right[0]
        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghz1 = event.ezp_R_E = event.ezp_R_M = event.ezp_R_T = 1
        event.ghzzp1 = 1j
        SMR_im[0] = event.computeP() - SM[0] - right[0]

        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghz1_prime2 = 1
        L1[0] = event.computeP()
        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghzgs1_prime2 = 1
        L1Zg[0] = event.computeP()

        ghz1_prime2_mix = -12110.20
        ghzgs1_prime2_mix = -7613.351302119843
        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghz1 = 1
        event.ghz1_prime2 = ghz1_prime2_mix
        event.ghzgs1_prime2 = ghzgs1_prime2_mix
        fa1fL1fL1Zg0p33[0] = event.computeP()

        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghz1 = 1 + M_Z**2 * ghz1_prime2_mix
        event.ghzzp1 = M_Z**2
        event.ezp_L_E = ezp_L_M = ezp_L_T = gZeL * ghz1_prime2_mix + e * ghzgs1_prime2_mix
        event.ezp_R_E = ezp_R_M = ezp_R_T = gZeR * ghz1_prime2_mix + e * ghzgs1_prime2_mix
        fa1fL1fL1Zg0p33_positive[0] = event.computeP()

        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghz1 = 1 + M_Z**2 * ghz1_prime2_mix
        event.ghzzp1 = M_Z**2
        event.ezp_L_E = ezp_L_M = ezp_L_T = gZeL * ghz1_prime2_mix - e * ghzgs1_prime2_mix
        event.ezp_R_E = ezp_R_M = ezp_R_T = gZeR * ghz1_prime2_mix - e * ghzgs1_prime2_mix
        fa1fL1fL1Zg0p33_negative[0] = event.computeP()

        D_L[0] = left[0]/leftxsec / (left[0]/leftxsec + SM[0]/SMxsec)
        D_R[0] = right[0]/rightxsec / (right[0]/rightxsec + SM[0]/SMxsec)
        try:
            D_LR[0] = left[0]/leftxsec / (left[0]/leftxsec + right[0]/rightxsec)
            D_LRint[0] = LR[0]/sqrt(leftxsec*rightxsec) / (left[0]/leftxsec + right[0]/rightxsec)
        except ZeroDivisionError:
            D_LR[0] = D_LRLR[0] = 0

        m4l[0], m1[0], m2[0], costheta1[0], costheta2[0], phi[0], costhetastar[0], phi1[0] = event.computeDecayAngles()

        if abs(m1[0] - M_Z) > abs(m2[0] - M_Z): m1[0], m2[0] = m2[0], m1[0]

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
