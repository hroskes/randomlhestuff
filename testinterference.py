#!/usr/bin/env python

import ROOT
SM, L, R = (-1.01396946768+0.0551089908689j), (0.541375132608), (-0.465609601233)

SMfactor = abs(SM)**2
Lfactor = L**2
Rfactor = R**2

SMLRefactor = SM.real * L
SMLImfactor = SM.imag * L

SMRRefactor = SM.real * R
SMRImfactor = SM.imag * R

LRfactor = L*R

f = ROOT.TFile("../lhefiles/batch2/left.root")
t = f.candTree

for i in range(20):
  t.GetEntry(i)

  print t.fL10p5/ (
        sum
       ((SMfactor    * t.SM,
       + Lfactor     * t.left,
       + Rfactor     * t.right,
       + SMLRefactor * t.SML,
       + SMLImfactor * t.SML_im,
       + SMRRefactor * t.SMR,
       + SMRImfactor * t.SMR_im,
       + LRfactor    * t.LR))
  )
