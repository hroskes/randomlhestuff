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
    int_im = array('d', [0])
    SM = array('d', [0])
    L1 = array('d', [0])
    L1Zg = array('d', [0])
    left_L1L1Zg = array('d', [0])
    right_L1L1Zg = array('d', [0])
    D_L = array('d', [0])
    D_R = array('d', [0])
    D_LR = array('d', [0])
    D_LRint = array('d', [0])
    costhetastar = array('d', [0])
    costheta1 = array('d', [0])
    costheta2 = array('d', [0])
    phi = array('d', [0])
    phi1 = array('d', [0])
    m1 = array('d', [0])
    m2 = array('d', [0])
    m4l = array('d', [0])

    leftE = array('d', [0])
    leftT = array('d', [0])
    rightE = array('d', [0])
    rightT = array('d', [0])
    leftrightE = array('d', [0])
    leftrightT = array('d', [0])
    leftTrightE = array('d', [0])
    leftErightT = array('d', [0])

    t.Branch("costhetastar", costhetastar, "costhetastar/D")
    t.Branch("costheta1", costheta1, "costheta1/D")
    t.Branch("costheta2", costheta2, "costheta2/D")
    t.Branch("phi", phi, "phi/D")
    t.Branch("phi1", phi1, "phi1/D")
    t.Branch("m1", m1, "m1/D")
    t.Branch("m2", m2, "m2/D")
    t.Branch("m4l", m4l, "m4l/D")
    t.Branch("left", left, "left/D")
    t.Branch("right", right, "right/D")
    t.Branch("SM", SM, "SM/D")
    t.Branch("int", int, "int/D")
    t.Branch("int_im", int_im, "int_im/D")
    t.Branch("L1", L1, "L1/D")
    t.Branch("L1Zg", L1Zg, "L1Zg/D")
    t.Branch("left_L1L1Zg", left_L1L1Zg, "left_L1L1Zg/D")
    t.Branch("right_L1L1Zg", right_L1L1Zg, "right_L1L1Zg/D")
    t.Branch("D_L", D_L, "D_L/D")
    t.Branch("D_R", D_R, "D_R/D")
    t.Branch("D_LR", D_LR, "D_LR/D")
    t.Branch("D_LRint", D_LRint, "D_LRint/D")

    t.Branch("leftE", leftE, "leftE/D")
    t.Branch("leftT", leftT, "leftT/D")
    t.Branch("rightE", rightE, "rightE/D")
    t.Branch("rightT", rightT, "rightT/D")
    t.Branch("leftrightE", leftrightE, "leftrightE/D")
    t.Branch("leftrightT", leftrightT, "leftrightT/D")
    t.Branch("leftTrightE", leftTrightE, "leftTrightE/D")
    t.Branch("leftErightT", leftErightT, "leftErightT/D")

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
        event.ghzzp1 = event.ezp_L_E = event.ezp_L_M = 1
        leftE[0] = event.computeP()
        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghzzp1 = event.ezp_L_T = 1
        leftT[0] = event.computeP()

        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghzzp1 = event.ezp_R_E = event.ezp_R_M = event.ezp_R_T = 1
        right[0] = event.computeP()
        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghzzp1 = event.ezp_R_E = event.ezp_R_M = 1
        rightE[0] = event.computeP()
        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghzzp1 = event.ezp_R_T = 1
        rightT[0] = event.computeP()

        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghzzp1 = event.ezp_L_E = event.ezp_L_M = event.ezp_R_T = 1
        leftErightT[0] = event.computeP()
        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghzzp1 = event.ezp_R_E = event.ezp_R_M = event.ezp_L_T = 1
        leftTrightE[0] = event.computeP()

        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghzzp1 = event.ezp_L_E = event.ezp_L_M = event.ezp_R_E = event.ezp_R_M = 1
        leftrightE[0] = event.computeP()
        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghzzp1 = event.ezp_L_T = event.ezp_R_T = 1
        leftrightT[0] = event.computeP()

        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghzzp1 = event.ezp_R_E = event.ezp_R_M = event.ezp_R_T = event.ezp_L_E = event.ezp_L_M = event.ezp_L_T = 1
        int[0] = event.computeP() - left[0] - right[0]
        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghzzp1 = event.ezp_R_E = event.ezp_R_M = event.ezp_R_T = 1
        event.ezp_L_E = event.ezp_L_M = event.ezp_L_T = 1j
        int_im[0] = event.computeP() - left[0] - right[0]
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
        event.ghz1, event.ghz1_prime2, event.ghzgs1_prime2 = a1forleft, g1prime2forleft, ghzgs1prime2forleft
        left_L1L1Zg[0] = event.computeP()

        event.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
        event.ghz1, event.ghz1_prime2, event.ghzgs1_prime2 = a1forright, g1prime2forright, ghzgs1prime2forright
        right_L1L1Zg[0] = event.computeP()

        left[0] /= leftxsec
        right[0] /= rightxsec
        int[0] /= sqrt(leftxsec*rightxsec)
        int_im[0] /= sqrt(leftxsec*rightxsec)
        SM[0] /= SMxsec
        L1[0] /= L1xsec
        L1Zg[0] /= L1Zgxsec

        D_L[0] = left[0] / (left[0] + SM[0])
        D_R[0] = right[0] / (right[0] + SM[0])
        try:
            D_LR[0] = left[0] / (left[0] + right[0])
            D_LRint[0] = int[0] / (left[0] + right[0])
        except ZeroDivisionError:
            D_LR[0] = D_LRint[0] = 0

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
