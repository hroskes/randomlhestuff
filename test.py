#!/usr/bin/env python
from mela import Mela, TVar

event = """
<event>
 9   0   1.0000000E+00   6.2499553E+01   7.8125000E-03   1.3828638E-01
       21   -1    0    0  501  502  0.00000000000E+00  0.00000000000E+00  5.37086667033E+02  5.37086667033E+02  0.00000000000E+00 0.00000000000E+00  1.
       21   -1    0    0  502  501  0.00000000000E+00  0.00000000000E+00 -7.27293062837E+00  7.27293062837E+00  0.00000000000E+00 0.00000000000E+00  1.
       25    2    1    2    0    0  2.66453525910E-15  0.00000000000E+00  5.29813736405E+02  5.44359597662E+02  1.24999105129E+02 0.00000000000E+00  1.
       23    2    3    3    0    0 -1.07287063341E+00  2.03413884495E+01  2.12763358296E+02  2.18095469074E+02  4.33873698414E+01 0.00000000000E+00  1.
       23    2    3    3    0    0  1.07287063341E+00 -2.03413884495E+01  3.17050378109E+02  3.26264128588E+02  7.42456477420E+01 0.00000000000E+00  1.
       11    1    4    4    0    0 -4.96385765951E+00  1.62933935971E+01  2.11696003997E+02  2.12380113632E+02  5.10998597706E-04 0.00000000000E+00  1.
      -11    1    4    4    0    0  3.89098702611E+00  4.04799485238E+00  1.06735429842E+00  5.71535544142E+00  5.10999912595E-04 0.00000000000E+00  1.
       13    1    5    5    0    0  8.04215953543E+00 -2.29213235677E+01  2.77968427622E+01  3.69151442044E+01  4.63538696652E-06 0.00000000000E+00  1.
      -13    1    5    5    0    0 -6.96928890202E+00  2.57993511828E+00  2.89253535347E+02  2.89348984384E+02  5.39479660939E-06 0.00000000000E+00  1.
</event>
"""

m = Mela()

m.setInputEvent_fromLHE(event.format(id1=11, id2=13), True)

M_Z = 91.1876
Ga_Z = 2.4952
aL = -0.53762
aR = 0.46238
e = 0.8431872482432357  # = cL_lep = cR_lep from mod_Parameters
L1 = 10000.

def ME(ghz1, ghz1_prime2, ghzgs1_prime2):
  m.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
  m.ghz1 = ghz1
  m.ghz1_prime2 = ghz1_prime2
  m.ghzgs1_prime2 = ghzgs1_prime2
  me1 = m.computeP()

  #note we only use the imaginary mZ^2 in ghz1
  #the one in ghzzp1 is to cancel this mZ^2
  #https://github.com/JHUGen/JHUGen/blob/4b0ae4d846846d90e2d8aad1dbb2279bbac9e416/JHUGenerator/mod_Higgs.F90#L952
  #so it's still real
  m.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZINDEPENDENT)
  m.ghz1 = ghz1 + 2 * ghz1_prime2 * (M_Z**2 - 1j*M_Z*Ga_Z)/L1**2
  m.ghzzp1 = M_Z**2/L1**2
  m.ezp_L_E = m.ezp_L_M = aL * ghz1_prime2 + e * ghzgs1_prime2
  m.ezp_R_E = m.ezp_R_M = aR * ghz1_prime2 + e * ghzgs1_prime2
  print m.ghz1, m.ghzzp1*m.ezp_L_E, m.ghzzp1*m.ezp_R_E
  me2 = m.computeP()

  print me1, me2


#when used with ghz1 = 1, these give fL1 or fL1Zg = 0.5
ghz1_prime2_mix = -12110.20
ghzgs1_prime2_mix = -7613.351302119843

print "SM"
ME(1, 0, 0)
print "L1"
ME(0, 1, 0)
print "L1Zg"
ME(0, 0, 1)
print "fL1=+0.5"
ME(1, ghz1_prime2_mix, 0)
print "fL1=-0.5"
ME(1, -ghz1_prime2_mix, 0)
print "fL1Zg=+0.5"
ME(1, 0, ghzgs1_prime2_mix)
print "fL1Zg=-0.5"
ME(1, 0, -ghzgs1_prime2_mix)
print "fa1 = fL1 = fL1Zg = 0.333"
ME(1, ghz1_prime2_mix, ghzgs1_prime2_mix)
