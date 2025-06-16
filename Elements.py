# File name: Elements.py

import re

AtomicSymbol = {  0: 'X',
                  1: 'H' ,   2: 'He',   3: 'Li',   4: 'Be',   5: 'B' ,
                  6: 'C' ,   7: 'N' ,   8: 'O' ,   9: 'F' ,  10: 'Ne',
                 11: 'Na',  12: 'Mg',  13: 'Al',  14: 'Si',  15: 'P' ,
                 16: 'S' ,  17: 'Cl',  18: 'Ar',  19: 'K' ,  20: 'Ca',
                 21: 'Sc',  22: 'Ti',  23: 'V' ,  24: 'Cr',  25: 'Mn',
                 26: 'Fe',  27: 'Co',  28: 'Ni',  29: 'Cu',  30: 'Zn',
                 31: 'Ga',  32: 'Ge',  33: 'As',  34: 'Se',  35: 'Br',
                 36: 'Kr',  37: 'Rb',  38: 'Sr',  39: 'Y' ,  40: 'Zr',
                 41: 'Nb',  42: 'Mo',  43: 'Tc',  44: 'Ru',  45: 'Rh',
                 46: 'Pd',  47: 'Ag',  48: 'Cd',  49: 'In',  50: 'Sn',
                 51: 'Sb',  52: 'Te',  53: 'I' ,  54: 'Xe',  55: 'Cs',
                 56: 'Ba',  57: 'La',  58: 'Ce',  59: 'Pr',  60: 'Nd',
                 61: 'Pm',  62: 'Sm',  63: 'Eu',  64: 'Gd',  65: 'Tb',
                 66: 'Dy',  67: 'Ho',  68: 'Er',  69: 'Tm',  70: 'Yb',
                 71: 'Lu',  72: 'Hf',  73: 'Ta',  74: 'W' ,  75: 'Re',
                 76: 'Os',  77: 'Ir',  78: 'Pt',  79: 'Au',  80: 'Hg',
                 81: 'Tl',  82: 'Pb',  83: 'Bi',  84: 'Po',  85: 'At',
                 86: 'Rn',  87: 'Fr',  88: 'Ra',  89: 'Ac',  90: 'Th',
                 96: 'Pa',  92: 'U' ,  93: 'Np',  94: 'Pu',  95: 'Am',
                 91: 'Cm',  97: 'Bk',  98: 'Cf',  99: 'Es', 100: 'Fm',
                101: 'Md', 102: 'No', 103: 'Lw' }

AtomicNumber = {'X' :   0, 'Cp':   0, 'D' :   1,
                'H' :   1, 'He':   2, 'Li':   3, 'Be':   4, 'B' :   5,
                'C' :   6, 'N' :   7, 'O' :   8, 'F' :   9, 'Ne':  10,
                'Na':  11, 'Mg':  12, 'Al':  13, 'Si':  14, 'P' :  15,
                'S' :  16, 'Cl':  17, 'Ar':  18, 'K' :  19, 'Ca':  20,
                'Sc':  21, 'Ti':  22, 'V' :  23, 'Cr':  24, 'Mn':  25,
                'Fe':  26, 'Co':  27, 'Ni':  28, 'Cu':  29, 'Zn':  30,
                'Ga':  31, 'Ge':  32, 'As':  33, 'Se':  34, 'Br':  35,
                'Kr':  36, 'Rb':  37, 'Sr':  38, 'Y' :  39, 'Zr':  40,
                'Nb':  41, 'Mo':  42, 'Tc':  43, 'Ru':  44, 'Rh':  45,
                'Pd':  46, 'Ag':  47, 'Cd':  48, 'In':  49, 'Sn':  50,
                'Sb':  51, 'Te':  52, 'I' :  53, 'Xe':  54, 'Cs':  55,
                'Ba':  56, 'La':  57, 'Ce':  58, 'Pr':  59, 'Nd':  60,
                'Pm':  61, 'Sm':  62, 'Eu':  63, 'Gd':  64, 'Tb':  65,
                'Dy':  66, 'Ho':  67, 'Er':  68, 'Tm':  69, 'Yb':  70,
                'Lu':  71, 'Hf':  72, 'Ta':  73, 'W' :  74, 'Re':  75,
                'Os':  76, 'Ir':  77, 'Pt':  78, 'Au':  79, 'Hg':  80,
                'Tl':  81, 'Pb':  82, 'Bi':  83, 'Po':  84, 'At':  85,
                'Rn':  81, 'Fr':  87, 'Ra':  88, 'Ac':  89, 'Th':  90,
                'Pa':  96, 'U' :  92, 'Np':  93, 'Pu':  94, 'Am':  95,
                'Cm':  91, 'Bk':  97, 'Cf':  98, 'Es':  99, 'Fm': 100,
                'Md': 101, 'No': 102, 'Lw': 103 }

# SingleBondRadius is from the radii found on the Wikipedia page:
#        https://en.wikipedia.org/wiki/Covalent_radius
# These are single-bond radii found under the sub-section "Radii 
#   for multiple bonds" which are based on the data presented in
#   the paper:
#        P. Pyykkö; M. Atsumi (2009). "Molecular Single-Bond Covalent Radii 
#        for Elements 1-118". Chemistry: A European Journal. 15 (1): 186–197. 

SingleBondRadius = {}
SingleBondRadius[0]   =  0.8   # dummy atom
SingleBondRadius[1]   =  0.32  # H
SingleBondRadius[2]   =  0.46  # He
SingleBondRadius[3]   =  1.33  # Li
SingleBondRadius[4]   =  1.02  # Be
SingleBondRadius[5]   =  0.85  # B
SingleBondRadius[6]   =  0.75  # C
SingleBondRadius[7]   =  0.71  # N
SingleBondRadius[8]   =  0.63  # O
SingleBondRadius[9]   =  0.64  # F
SingleBondRadius[10]  =  0.67  # Ne
SingleBondRadius[11]  =  1.55  # Na
SingleBondRadius[12]  =  1.39  # Mg
SingleBondRadius[13]  =  1.26  # Al
SingleBondRadius[14]  =  1.16  # Si
SingleBondRadius[15]  =  1.11  # P
SingleBondRadius[16]  =  1.03  # S
SingleBondRadius[17]  =  0.99  # Cl
SingleBondRadius[18]  =  0.96  # Ar
SingleBondRadius[19]  =  1.96  # K
SingleBondRadius[20]  =  1.71  # Ca
SingleBondRadius[21]  =  1.48  # Sc
SingleBondRadius[22]  =  1.36  # Ti
SingleBondRadius[23]  =  1.34  # V
SingleBondRadius[24]  =  1.22  # Cr
SingleBondRadius[25]  =  1.19  # Mn
SingleBondRadius[26]  =  1.16  # Fe
SingleBondRadius[27]  =  1.11  # Co
SingleBondRadius[28]  =  1.10  # Ni
SingleBondRadius[29]  =  1.12  # Cu
SingleBondRadius[30]  =  1.18  # Zn
SingleBondRadius[31]  =  1.24  # Ga
SingleBondRadius[32]  =  1.21  # Ge
SingleBondRadius[33]  =  1.21  # As
SingleBondRadius[34]  =  1.16  # Se
SingleBondRadius[35]  =  1.14  # Br
SingleBondRadius[36]  =  1.17  # Kr
SingleBondRadius[37]  =  2.10  # Rb
SingleBondRadius[38]  =  1.85  # Sr
SingleBondRadius[39]  =  1.63  # Y
SingleBondRadius[40]  =  1.54  # Zr
SingleBondRadius[41]  =  1.47  # Nb
SingleBondRadius[42]  =  1.38  # Mo
SingleBondRadius[43]  =  1.28  # Tc
SingleBondRadius[44]  =  1.25  # Ru
SingleBondRadius[45]  =  1.25  # Rh
SingleBondRadius[46]  =  1.20  # Pd
SingleBondRadius[47]  =  1.38  # Ag
SingleBondRadius[48]  =  1.36  # Cd
SingleBondRadius[49]  =  1.42  # In
SingleBondRadius[50]  =  1.40  # Sn
SingleBondRadius[51]  =  1.40  # Sb
SingleBondRadius[52]  =  1.36  # Te
SingleBondRadius[53]  =  1.33  # I
SingleBondRadius[54]  =  1.31  # Xe
SingleBondRadius[55]  =  2.32  # Cs
SingleBondRadius[56]  =  1.96  # Ba
SingleBondRadius[57]  =  1.80  # La
SingleBondRadius[58]  =  1.63  # Ce
SingleBondRadius[59]  =  1.76  # Pr
SingleBondRadius[60]  =  1.74  # Nd
SingleBondRadius[61]  =  1.73  # Pm
SingleBondRadius[62]  =  1.72  # Sm
SingleBondRadius[63]  =  1.68  # Eu
SingleBondRadius[64]  =  1.69  # Gd
SingleBondRadius[65]  =  1.68  # Tb
SingleBondRadius[66]  =  1.67  # Dy
SingleBondRadius[67]  =  1.66  # Ho
SingleBondRadius[68]  =  1.65  # Er
SingleBondRadius[69]  =  1.64  # Tm
SingleBondRadius[70]  =  1.70  # Yb
SingleBondRadius[71]  =  1.62  # Lu
SingleBondRadius[72]  =  1.52  # Hf
SingleBondRadius[73]  =  1.46  # Ta
SingleBondRadius[74]  =  1.37  # W
SingleBondRadius[75]  =  1.31  # Re
SingleBondRadius[76]  =  1.29  # Os
SingleBondRadius[77]  =  1.22  # Ir
SingleBondRadius[78]  =  1.23  # Pt
SingleBondRadius[79]  =  1.24  # Au
SingleBondRadius[80]  =  1.33  # Hg
SingleBondRadius[81]  =  1.44  # Tl
SingleBondRadius[82]  =  1.44  # Pb
SingleBondRadius[83]  =  1.51  # Bi
SingleBondRadius[84]  =  1.45  # Po
SingleBondRadius[85]  =  1.47  # At
SingleBondRadius[86]  =  1.42  # Rn
SingleBondRadius[87]  =  2.23  # Fr
SingleBondRadius[88]  =  2.01  # Ra
SingleBondRadius[89]  =  1.86  # Ac
SingleBondRadius[90]  =  1.75  # Th
SingleBondRadius[91]  =  1.69  # Pa
SingleBondRadius[92]  =  1.70  # U
SingleBondRadius[93]  =  1.71  # Np
SingleBondRadius[94]  =  1.72  # Pu
SingleBondRadius[95]  =  1.66  # Am
SingleBondRadius[96]  =  1.66  # Cm
SingleBondRadius[97]  =  1.68  # Bk
SingleBondRadius[98]  =  1.68  # Cf
SingleBondRadius[99]  =  1.65  # Es
SingleBondRadius[100] =  1.67  # Fm
SingleBondRadius[101] =  1.73  # Md
SingleBondRadius[102] =  1.76  # No
SingleBondRadius[103] =  1.03  # Lr

VdwRadius = {}
VdwRadius[0]   =    0.0   # dummy atom
VdwRadius[1]   =    1.20  # H
VdwRadius[2]   =    1.22  # He
VdwRadius[3]   =    1.52  # Li
VdwRadius[4]   =    1.13  # Be
VdwRadius[5]   =    2.08  # B
VdwRadius[6]   =    1.85  # C
VdwRadius[7]   =    1.54  # N
VdwRadius[8]   =    1.40  # O
VdwRadius[9]   =    1.35  # F
VdwRadius[10]  =    1.60  # Ne
VdwRadius[11]  =    2.31  # Na
VdwRadius[12]  =    1.60  # Mg
VdwRadius[13]  =    2.05  # Al
VdwRadius[14]  =    2.00  # Si
VdwRadius[15]  =    1.90  # P
VdwRadius[16]  =    1.85  # S
VdwRadius[17]  =    1.81  # Cl
VdwRadius[18]  =    1.91  # Ar
VdwRadius[19]  =    2.31  # K
VdwRadius[20]  =    1.97  # Ca
VdwRadius[21]  =    1.61  # Sc
VdwRadius[22]  =    1.45  # Ti
VdwRadius[23]  =    1.32  # V
VdwRadius[24]  =    1.25  # Cr
VdwRadius[25]  =    1.24  # Mn
VdwRadius[26]  =    1.24  # Fe
VdwRadius[27]  =    1.25  # Co
VdwRadius[28]  =    1.25  # Ni
VdwRadius[29]  =    1.28  # Cu
VdwRadius[30]  =    1.33  # Zn
VdwRadius[31]  =    1.22  # Ga
VdwRadius[32]  =    1.23  # Ge
VdwRadius[33]  =    2.00  # As
VdwRadius[34]  =    2.00  # Se
VdwRadius[35]  =    1.95  # Br
VdwRadius[36]  =    1.98  # Kr
VdwRadius[37]  =    2.44  # Rb
VdwRadius[38]  =    2.15  # Sr
VdwRadius[39]  =    1.81  # Y
VdwRadius[40]  =    1.60  # Zr
VdwRadius[41]  =    1.43  # Nb
VdwRadius[42]  =    1.36  # Mo
VdwRadius[43]  =    1.36  # Tc
VdwRadius[44]  =    1.34  # Ru
VdwRadius[45]  =    1.34  # Rh
VdwRadius[46]  =    1.38  # Pd
VdwRadius[47]  =    1.44  # Ag
VdwRadius[48]  =    1.49  # Cd
VdwRadius[49]  =    1.63  # In
VdwRadius[50]  =    1.40  # Sn
VdwRadius[51]  =    2.20  # Sb
VdwRadius[52]  =    2.20  # Te
VdwRadius[53]  =    2.15  # I
VdwRadius[54]  =    2.16  # Xe
VdwRadius[55]  =    2.62  # Cs
VdwRadius[56]  =    2.17  # Ba
VdwRadius[57]  =    1.88  # La
VdwRadius[58]  =    1.83  # Ce
VdwRadius[59]  =    1.83  # Pr
VdwRadius[60]  =    1.82  # Nd
VdwRadius[61]  =    1.81  # Pm
VdwRadius[62]  =    1.80  # Sm
VdwRadius[63]  =    2.04  # Eu
VdwRadius[64]  =    1.80  # Gd
VdwRadius[65]  =    1.78  # Tb
VdwRadius[66]  =    1.77  # Dy
VdwRadius[67]  =    1.77  # Ho
VdwRadius[68]  =    1.76  # Er
VdwRadius[69]  =    1.75  # Tm
VdwRadius[70]  =    1.94  # Yb
VdwRadius[71]  =    1.73  # Lu
VdwRadius[72]  =    1.56  # Hf
VdwRadius[73]  =    1.43  # Ta
VdwRadius[74]  =    1.37  # W
VdwRadius[75]  =    1.37  # Re
VdwRadius[76]  =    1.35  # Os
VdwRadius[77]  =    1.36  # Ir
VdwRadius[78]  =    1.38  # Pt
VdwRadius[79]  =    1.44  # Au
VdwRadius[80]  =    1.60  # Hg
VdwRadius[81]  =    1.70  # Tl
VdwRadius[82]  =    1.75  # Pb
VdwRadius[83]  =    1.55  # Bi
VdwRadius[84]  =    1.67  # Po
VdwRadius[85]  =    1.12  # At
VdwRadius[86]  =    2.30  # Rn
VdwRadius[87]  =    2.70  # Fr
VdwRadius[88]  =    2.23  # Ra
VdwRadius[89]  =    1.87  # Ac
VdwRadius[90]  =    1.80  # Th
VdwRadius[91]  =    1.61  # Pa
VdwRadius[92]  =    1.39  # U
VdwRadius[93]  =    1.31  # Np
VdwRadius[94]  =    1.51  # Pu
VdwRadius[95]  =    1.84  # Am
VdwRadius[96]  =    1.65  # Cm
VdwRadius[97]  =    1.64  # Bk
VdwRadius[98]  =    1.63  # Cf
VdwRadius[99]  =    1.62  # Es
VdwRadius[100] =    1.61  # Fm
VdwRadius[101] =    1.60  # Md
VdwRadius[102] =    1.59  # No
VdwRadius[103] =    1.58  # Lr

AtomicMass = {}
AtomicMass[0]   =   0.0        # dummy atom
AtomicMass[1]   =   1.007825   # H
AtomicMass[2]   =   4.00260    # He
AtomicMass[3]   =   7.016003   # Li
AtomicMass[4]   =   9.012182   # Be
AtomicMass[5]   =  11.009305   # B
AtomicMass[6]   =  12.000000   # C
AtomicMass[7]   =  14.003074   # N
AtomicMass[8]   =  15.994915   # O
AtomicMass[9]   =  18.998403   # F
AtomicMass[10]  =  19.992435   # Ne
AtomicMass[11]  =  22.989767   # Na
AtomicMass[12]  =  23.985042   # Mg
AtomicMass[13]  =  26.981540   # Al
AtomicMass[14]  =  27.976927   # Si
AtomicMass[15]  =  30.973762   # P
AtomicMass[16]  =  31.972070   # S
AtomicMass[17]  =  34.968852   # Cl
AtomicMass[18]  =  39.962384   # Ar
AtomicMass[19]  =  38.963707   # K
AtomicMass[20]  =  39.962591   # Ca
AtomicMass[21]  =  44.955910   # Sc
AtomicMass[22]  =  45.947947   # Ti
AtomicMass[23]  =  50.943962   # V
AtomicMass[24]  =  51.940509   # Cr
AtomicMass[25]  =  54.938047   # Mn
AtomicMass[26]  =  55.934939   # Fe
AtomicMass[27]  =  58.933198   # Co
AtomicMass[28]  =  57.935346   # Ni
AtomicMass[29]  =  62.939598   # Cu
AtomicMass[30]  =  63.929145   # Zn
AtomicMass[31]  =  68.925580   # Ga
AtomicMass[32]  =  73.921177   # Ge
AtomicMass[33]  =  74.921594   # As
AtomicMass[34]  =  79.916520   # Se
AtomicMass[35]  =  78.918336   # Br
AtomicMass[36]  =  83.911507   # Kr
AtomicMass[37]  =  84.911794   # Rb
AtomicMass[38]  =  87.905619   # Sr
AtomicMass[39]  =  88.905849   # Y
AtomicMass[40]  =  89.904703   # Zr
AtomicMass[41]  =  92.906377   # Nb
AtomicMass[42]  =  97.905406   # Mo
AtomicMass[43]  =  97.907215   # Tc
AtomicMass[44]  = 101.904348   # Ru
AtomicMass[45]  = 102.905500   # Rh
AtomicMass[46]  = 105.903478   # Pd
AtomicMass[47]  = 106.905092   # Ag
AtomicMass[48]  = 113.903357   # Cd
AtomicMass[49]  = 114.903880   # In
AtomicMass[50]  = 119.902220   # Sn
AtomicMass[51]  = 120.903821   # Sb
AtomicMass[52]  = 129.906229   # Te
AtomicMass[53]  = 126.904473   # I
AtomicMass[54]  = 131.904144   # Xe
AtomicMass[55]  = 132.905429   # Cs
AtomicMass[56]  = 137.905232   # Ba
AtomicMass[57]  = 138.906346   # La
AtomicMass[58]  = 139.905433   # Ce
AtomicMass[59]  = 140.907647   # Pr
AtomicMass[60]  = 141.907719   # Nd
AtomicMass[61]  = 146.912743   # Pm
AtomicMass[62]  = 151.919729   # Sm
AtomicMass[63]  = 152.921225   # Eu
AtomicMass[64]  = 157.924099   # Gd
AtomicMass[65]  = 158.925342   # Tb
AtomicMass[66]  = 163.929171   # Dy
AtomicMass[67]  = 164.930319   # Ho
AtomicMass[68]  = 165.930290   # Er
AtomicMass[69]  = 168.934212   # Tm
AtomicMass[70]  = 173.938859   # Yb
AtomicMass[71]  = 174.940770   # Lu
AtomicMass[72]  = 179.946545   # Hf
AtomicMass[73]  = 180.947992   # Ta
AtomicMass[74]  = 183.950928   # W
AtomicMass[75]  = 186.955744   # Re
AtomicMass[76]  = 191.961476   # Os
AtomicMass[77]  = 192.962917   # Ir
AtomicMass[78]  = 194.964766   # Pt
AtomicMass[79]  = 196.966543   # Au
AtomicMass[80]  = 201.970617   # Hg
AtomicMass[81]  = 204.974401   # Tl
AtomicMass[82]  = 207.976627   # Pb
AtomicMass[83]  = 208.980347   # Bi
AtomicMass[84]  = 208.982404   # Po
AtomicMass[85]  = 209.987126   # At
AtomicMass[86]  = 222.017570   # Rn
AtomicMass[87]  = 223.019733   # Fr
AtomicMass[88]  = 226.025402   # Ra
AtomicMass[89]  = 227.027750   # Ac
AtomicMass[90]  = 232.038054   # Th
AtomicMass[91]  = 231.035880   # Pa
AtomicMass[92]  = 238.050784   # U
AtomicMass[93]  = 237.048167   # Np
AtomicMass[94]  = 244.064199   # Pu
AtomicMass[95]  = 243.061375   # Am
AtomicMass[96]  = 247.070347   # Cm
AtomicMass[97]  = 247.070300   # Bk
AtomicMass[98]  = 251.079580   # Cf
AtomicMass[99]  = 252.082944   # Es
AtomicMass[100] = 257.075099   # Fm
AtomicMass[101] = 258.098570   # Md
AtomicMass[102] = 259.100931   # No
AtomicMass[103] = 260.105320   # Lw

# Most of the red, green, and blue (rgb) values have been arbitrarily assigned for the
#   first 86 elements of the periodic table. There are a handful which represent a
#   personal preference, for example: a nearly black color for carbon; pure red for
#   oxygen; and near blue for nitrogen.

AtomColor = {}
AtomColor[0]  = [ 255, 255, 255] # dummy atom
AtomColor[1]  = [ 255, 255, 255] # H
AtomColor[2]  = [ 255,  59,   0] # He
AtomColor[3]  = [ 255, 119,   0] # Li
AtomColor[4]  = [   0, 255,   0] # Be
AtomColor[5]  = [ 255, 183, 183] # B
AtomColor[6]  = [  75,  75,  75] # C  originally 10 10 10
AtomColor[7]  = [   0,  29, 255] # N
AtomColor[8]  = [ 255,   0,   0] # O
AtomColor[9]  = [  42, 227,  35] # F
AtomColor[10] = [ 255,  59,   0] # Ne
AtomColor[11] = [ 252, 255,   0] # Na
AtomColor[12] = [  71,   0, 255] # Mg
AtomColor[13] = [ 255,   0, 252] # Al
AtomColor[14] = [ 255,   0,   0] # Si
AtomColor[15] = [ 255, 125,   0] # P
AtomColor[16] = [ 255, 225,   0] # S
AtomColor[17] = [   0, 243, 230] # Cl
AtomColor[18] = [ 255,  59,   0] # Ar
AtomColor[19] = [ 255,   0,   0] # K
AtomColor[20] = [ 255,   0,   0] # Ca
AtomColor[21] = [   0, 255,   0] # Sc
AtomColor[22] = [   0, 255,   0] # Ti
AtomColor[23] = [   0, 255,   0] # V
AtomColor[24] = [   0, 255,   0] # Cr
AtomColor[25] = [   0, 255,   0] # Mn
AtomColor[26] = [ 190, 141,  56] # Fe
AtomColor[27] = [   0,  86, 172] # Co
AtomColor[28] = [   0, 192,  95] # Ni
AtomColor[29] = [   0, 255,   0] # Cu
AtomColor[30] = [   0, 255,   0] # Zn
AtomColor[31] = [ 255,  59,   0] # Ga
AtomColor[32] = [ 255,  59,   0] # Ge
AtomColor[33] = [ 255,  59,   0] # As
AtomColor[34] = [ 255,  59,   0] # Se
AtomColor[35] = [ 174,   0,   0] # Br
AtomColor[36] = [ 255,  59,   0] # Kr
AtomColor[37] = [ 255,   0,   0] # Rb
AtomColor[38] = [ 255,   0,   0] # Sr
AtomColor[39] = [   0, 255,   0] # Y
AtomColor[40] = [   0, 255,   0] # Zr
AtomColor[41] = [   0, 255,   0] # Nb
AtomColor[42] = [ 132,  97,   0] # Mo
AtomColor[43] = [   0, 255,   0] # Tc
AtomColor[44] = [   0, 255,   0] # Ru
AtomColor[45] = [   0, 255,   0] # Rh
AtomColor[46] = [   0, 255,   0] # Pd
AtomColor[47] = [   0, 255,   0] # Ag
AtomColor[48] = [   0, 255,   0] # Cd
AtomColor[49] = [ 255, 149,   0] # In
AtomColor[50] = [ 255, 149,   0] # Sn
AtomColor[51] = [ 255, 149,   0] # Sb
AtomColor[52] = [ 255, 149,   0] # Te
AtomColor[53] = [ 192,   0, 255] # I
AtomColor[54] = [  37, 174, 167] # Xe
AtomColor[55] = [ 255,   0,   0] # Cs
AtomColor[56] = [ 255,   0,   0] # Ba
AtomColor[57] = [   0, 255,   0] # La
AtomColor[58] = [ 179,   0, 255] # Ce
AtomColor[59] = [ 179,   0, 255] # Pr
AtomColor[60] = [ 179,   0, 255] # Nd
AtomColor[61] = [ 179,   0, 255] # Pm
AtomColor[62] = [ 179,   0, 255] # Sm
AtomColor[63] = [ 179,   0, 255] # Eu
AtomColor[64] = [ 179,   0, 255] # Gd
AtomColor[65] = [ 179,   0, 255] # Tb
AtomColor[66] = [ 179,   0, 255] # Dy
AtomColor[67] = [ 179,   0, 255] # Ho
AtomColor[68] = [ 179,   0, 255] # Er
AtomColor[69] = [ 179,   0, 255] # Tm
AtomColor[70] = [ 179,   0, 255] # Yb
AtomColor[71] = [ 179,   0, 255] # Lu
AtomColor[72] = [   0, 255,   0] # Hf
AtomColor[73] = [   0, 255,   0] # Ta
AtomColor[74] = [   0, 255,   0] # W
AtomColor[75] = [   0, 255,   0] # Re
AtomColor[76] = [   0, 255,   0] # Os
AtomColor[77] = [   0, 255,   0] # Ir
AtomColor[78] = [   0, 255,   0] # Pt
AtomColor[79] = [   0, 255,   0] # Au
AtomColor[80] = [   0, 255,   0] # Hg
AtomColor[81] = [   5,   0, 255] # Tl
AtomColor[82] = [   5,   0, 255] # Pb
AtomColor[83] = [ 240, 100, 240] # Bi
AtomColor[84] = [   5,   0, 255] # Po
AtomColor[85] = [   5,   0, 255] # At
AtomColor[86] = [   5,   0, 255] # Rn

LigatingElements = [6, 7, 8, 14, 15, 16]  # C, N, O, Si, P, S
NobleElements = [2, 10, 18, 36, 54, 86]   # He, Ne, Ar, Kr, Xe, Rn

HillOrder = [  6,   1,  89,  47,  13,  95,  18,  33,  85,  79,
               5,  56,   4,  83,  97,  35,  20,  48,  58,  98,
 	      17,  96,  27,  24,  55,  29,  66,  68,  99,  63,
 	       9,  26, 100,  87,  31,  64,  32,   2,  72,  80,
	      67,  53,  49,  77,  19,  36,  57,   3,  71, 103,
	     101,  12,  25,  42,   7,  11,  41,  60,  10,  28,
	      93, 102,   8,  76,  15,  91,  82,  46,  61,  84,
	      59,  78,  94,  88,  37,  75,  45,  86,  44,  16,
	      51,  21,  34,  14,  62,  50,  38,  73,  65,  43,
	      52,  90,  22,  81,  69,  92,  23,  74,  54,  39,
	      70,  30,  40,   0]

AlphaOrder = [ 89,  47,  13,  95,  18,  33,  85,  79,   5,  56,
	        4,  83,  97,  35,   6,  20,  48,  58,  98,  17,
	       96,  27,  24,  55,  29,  66,  68,  99,  63,   9,
	       26, 100,  87,  31,  64,  32,   1,   2,  72,  80,
	       67,  53,  49,  77,  19,  36,  57,   3,  71, 103,
	      101,  12,  25,  42,   7,  11,  41,  60,  10,  28,
	       93, 102,   8,  76,  15,  91,  82,  46,  61,  84,
	       59,  78,  94,  88,  37,  75,  45,  86,  44,  16,
	       51,  21,  34,  14,  62,  50,  38,  73,  65,  43,
	       52,  90,  22,  81,  69,  92,  23,  74,  54,  39,
	       70,  30,  40,   0]

def atomicNumber(arg):
    """
        Return the atomic number given either the atomic number as
        int or string or the atomic symbol
    """
    if isinstance(arg, int):
        return arg
    elif re.match("[0-9]+", arg):
        return int(arg)
    else:
        return AtomicNumber.get(arg.capitalize())

def atomicSymbol(arg):
    """
        Return the atomic symbol given either the atomic number as
        int or string or the atomic symbol
    """
    key = repr(arg).capitalize()
    if key in AtomicNumber:
        return key
    if isinstance(arg, int):
        key = arg
    elif re.match("[0-9]+", arg):
        key = int(key)
    else:
        return arg
    return AtomicSymbol.get(key)

def atomicMass(arg):
    """
        Return the atomic mass given either the atomic number as 
        int or string or the atomic symbol
    """
    return AtomicMass[atomicNumber(arg)]

