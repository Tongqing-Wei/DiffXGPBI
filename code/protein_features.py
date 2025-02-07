#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Bio import SeqIO
from collections import OrderedDict
import numpy as np
import pandas as pd
import re
import os


def walkFile(file):
    phage_name = []
    for root, dirs, files in os.walk(file):

        # root 	The path of the currently accessed folder
        # dirs 	list of subdirectories in this folder
        # files 	list of files under this folder
        # traversal file
        for f in files:
            phage_name.append(os.path.join(f))
    return phage_name

def protein_features(protein_sequences):
    """
    This function calculates a number of basic properties for a list of protein sequences
    
    Input: list of protein sequences (as strings), length can also be 1
    Output: a dataframe of features
    """
    
    import numpy as np
    import pandas as pd
    from Bio.SeqUtils.ProtParam import ProteinAnalysis
    from collections import Counter
    
    # AA frequency and protein characteristics
    mol_weight = []; aromaticity = []; instability = []; flexibility = []; prot_length = []
    pI = []; helix_frac = []; turn_frac = []; sheet_frac = []
    frac_aliph = []; frac_unch_polar = []; frac_polar = []; frac_hydrophob = []; frac_pos = []; frac_sulfur = []
    frac_neg = []; frac_amide = []; frac_alcohol = []; C2 = []; H2 = []; O2 = []; N2 = []; S2 = []
    AA_dict = {'G': [], 'A': [], 'V': [], 'L': [], 'I': [], 'F': [], 'P': [], 'S': [], 'T': [], 'Y': [],
           'Q': [], 'N': [], 'E': [], 'D': [], 'W': [], 'H': [], 'R': [], 'K': [], 'M': [], 'C': []}
    
    # calculate physical_chemical_feature
    for items in protein_sequences:
        items=items.replace('X','').replace('U','').replace('B','').replace('Z','').replace('*','')
        CE = 'CHONS'
        Chemi_stats = {'A':{'C': 3, 'H': 7, 'O': 2, 'N': 1, 'S': 0},
                       'C':{'C': 3, 'H': 7, 'O': 2, 'N': 1, 'S': 1},
                       'D':{'C': 4, 'H': 7, 'O': 4, 'N': 1, 'S': 0},
                       'E':{'C': 5, 'H': 9, 'O': 4, 'N': 1, 'S': 0},
                       'F':{'C': 9, 'H': 11,'O': 2, 'N': 1, 'S': 0},
                       'G':{'C': 2, 'H': 5, 'O': 2, 'N': 1, 'S': 0},
                       'H':{'C': 6, 'H': 9, 'O': 2, 'N': 3, 'S': 0},
                       'I':{'C': 6, 'H': 13,'O': 2, 'N': 1, 'S': 0},
                       'K':{'C': 6, 'H': 14,'O': 2, 'N': 2, 'S': 0},
                       'L':{'C': 6, 'H': 13,'O': 2, 'N': 1, 'S': 0},
                       'M':{'C': 5, 'H': 11,'O': 2, 'N': 1, 'S': 1},
                       'N':{'C': 4, 'H': 8, 'O': 3, 'N': 2, 'S': 0},
                       'P':{'C': 5, 'H': 9, 'O': 2, 'N': 1, 'S': 0},
                       'Q':{'C': 5, 'H': 10,'O': 3, 'N': 2, 'S': 0},
                       'R':{'C': 6, 'H': 14,'O': 2, 'N': 4, 'S': 0},
                       'S':{'C': 3, 'H': 7, 'O': 3, 'N': 1, 'S': 0},
                       'T':{'C': 4, 'H': 9, 'O': 3, 'N': 1, 'S': 0},
                       'V':{'C': 5, 'H': 11,'O': 2, 'N': 1, 'S': 0},
                       'W':{'C': 11,'H': 12,'O': 2, 'N': 2, 'S': 0},
                       'Y':{'C': 9, 'H': 11,'O': 3, 'N': 1, 'S': 0}
                    }
    
        count = Counter(items)
        code = []
    
        for c in CE:
            abundance_c = 0
            for key in count:
                num_c = Chemi_stats[key][c]
                abundance_c += num_c * count[key]
                
            code.append(abundance_c)
            
        C, H, O, N, S = code
        C2.append(C)
        H2.append(H)
        O2.append(O)
        N2.append(N)
        S2.append(S)

    
    for item in protein_sequences:
        item=item.replace('X','').replace('U','').replace('B','').replace('Z','').replace('*','')
        # calculate various protein properties
        prot_length.append(len(item))
        frac_aliph.append((item.count('A')+item.count('G')+item.count('I')+item.count('L')+item.count('P')
                       +item.count('V'))/len(item))
        frac_unch_polar.append((item.count('S')+item.count('T')+item.count('N')+item.count('Q'))/len(item))
        frac_polar.append((item.count('Q')+item.count('N')+item.count('H')+item.count('S')+item.count('T')+item.count('Y')
                      +item.count('C')+item.count('M')+item.count('W'))/len(item))
        frac_hydrophob.append((item.count('A')+item.count('G')+item.count('I')+item.count('L')+item.count('P')
                        +item.count('V')+item.count('F'))/len(item))
        frac_pos.append((item.count('H')+item.count('K')+item.count('R'))/len(item))
        frac_sulfur.append((item.count('C')+item.count('M'))/len(item))
        frac_neg.append((item.count('D')+item.count('E'))/len(item))
        frac_amide.append((item.count('N')+item.count('Q'))/len(item))
        frac_alcohol.append((item.count('S')+item.count('T'))/len(item))
        protein_chars = ProteinAnalysis(item) 
        mol_weight.append(protein_chars.molecular_weight())
        aromaticity.append(protein_chars.aromaticity())
        instability.append(protein_chars.instability_index())
        flexibility.append(np.mean(protein_chars.flexibility()))
        pI.append(protein_chars.isoelectric_point())
        H, T, S = protein_chars.secondary_structure_fraction()
        helix_frac.append(H)
        turn_frac.append(T)
        sheet_frac.append(S)
    
        # calculate AA frequency
        for key in AA_dict.keys():
            AA_dict[key].append(item.count(key)/len(item))
            
    # make new dataframe & return
    features_protein = pd.DataFrame.from_dict(AA_dict)
    features_protein['protein_length'] = np.asarray(prot_length)
    features_protein['mol_weight'] = np.asarray(mol_weight)
    features_protein['aromaticity'] = np.asarray(aromaticity)
    features_protein['instability'] = np.asarray(instability)
    features_protein['flexibility'] = np.asarray(flexibility)
    features_protein['pI'] = np.asarray(pI)
    features_protein['frac_aliphatic'] = np.asarray(frac_aliph)
    features_protein['frac_uncharged_polar'] = np.asarray(frac_unch_polar)
    features_protein['frac_polar'] = np.asarray(frac_polar)
    features_protein['frac_hydrophobic'] = np.asarray(frac_hydrophob)
    features_protein['frac_positive'] = np.asarray(frac_pos)
    features_protein['frac_sulfur'] = np.asarray(frac_sulfur)
    features_protein['frac_negative'] = np.asarray(frac_neg)
    features_protein['frac_amide'] = np.asarray(frac_amide)
    features_protein['frac_alcohol'] = np.asarray(frac_alcohol)
    features_protein['AA_frac_helix'] = np.asarray(helix_frac)
    features_protein['AA_frac_turn'] = np.asarray(turn_frac)
    features_protein['AA_frac_sheet'] = np.asarray(sheet_frac)
    features_protein['C2'] = np.asarray(C2)
    features_protein['H2'] = np.asarray(H2)
    features_protein['O2'] = np.asarray(O2)
    features_protein['N2'] = np.asarray(N2)
    features_protein['S2'] = np.asarray(S2)
    
    return features_protein


# PROTEIN FEATURE: COMPOSITION
# --------------------------------------------------
def Count1(seq1, seq2):
	sum = 0
	for aa in seq1:
		sum = sum + seq2.count(aa)
	return sum

# C/T/D model
def CTDC(sequence):
	group1 = {
		'hydrophobicity_PRAM900101': 'RKEDQN',
		'hydrophobicity_ARGP820101': 'QSTNGDE',
		'hydrophobicity_ZIMJ680101': 'QNGSWTDERA',
		'hydrophobicity_PONP930101': 'KPDESNQT',
		'hydrophobicity_CASG920101': 'KDEQPSRNTG',
		'hydrophobicity_ENGD860101': 'RDKENQHYP',
		'hydrophobicity_FASG890101': 'KERSQD',
		'normwaalsvolume': 'GASTPDC',
		'polarity':        'LIFWCMVY',
		'polarizability':  'GASDT',
		'charge':          'KR',
		'secondarystruct': 'EALMQKRH',
		'solventaccess':   'ALFCGIVW'
	}
	group2 = {
		'hydrophobicity_PRAM900101': 'GASTPHY',
		'hydrophobicity_ARGP820101': 'RAHCKMV',
		'hydrophobicity_ZIMJ680101': 'HMCKV',
		'hydrophobicity_PONP930101': 'GRHA',
		'hydrophobicity_CASG920101': 'AHYMLV',
		'hydrophobicity_ENGD860101': 'SGTAW',
		'hydrophobicity_FASG890101': 'NTPG',
		'normwaalsvolume': 'NVEQIL',
		'polarity':        'PATGS',
		'polarizability':  'CPNVEQIL',
		'charge':          'ANCQGHILMFPSTWYV',
		'secondarystruct': 'VIYCWFT',
		'solventaccess':   'RKQEND'
	}

	property = ['hydrophobicity_PRAM900101', 'hydrophobicity_ARGP820101', 'hydrophobicity_ZIMJ680101', 'hydrophobicity_PONP930101',
	'hydrophobicity_CASG920101', 'hydrophobicity_ENGD860101', 'hydrophobicity_FASG890101', 'normwaalsvolume',
	'polarity', 'polarizability', 'charge', 'secondarystruct', 'solventaccess']

	for p in property:
		c1 = Count1(group1[p], sequence) / len(sequence)
		c2 = Count1(group2[p], sequence) / len(sequence)
		c3 = 1 - c1 - c2
		encoding = [c1, c2, c3]
        
	return encoding


# PROTEIN FEATURE: TRANSITION
# --------------------------------------------------
def CTDT(sequence):
    """
    Every number in the encoding tells us as a percentage over all AA pairs, how many transitions
    occured from group x to y or vice versa for a specific property p.
    """
    group1 = {'hydrophobicity_PRAM900101': 'RKEDQN','hydrophobicity_ARGP820101': 'QSTNGDE',
              'hydrophobicity_ZIMJ680101': 'QNGSWTDERA','hydrophobicity_PONP930101': 'KPDESNQT',
              'hydrophobicity_CASG920101': 'KDEQPSRNTG','hydrophobicity_ENGD860101': 'RDKENQHYP',
              'hydrophobicity_FASG890101': 'KERSQD','normwaalsvolume': 'GASTPDC','polarity': 'LIFWCMVY',
              'polarizability': 'GASDT','charge':'KR', 'secondarystruct': 'EALMQKRH','solventaccess': 'ALFCGIVW'}
    
    group2 = {'hydrophobicity_PRAM900101': 'GASTPHY','hydrophobicity_ARGP820101': 'RAHCKMV',
           'hydrophobicity_ZIMJ680101': 'HMCKV','hydrophobicity_PONP930101': 'GRHA',
           'hydrophobicity_CASG920101': 'AHYMLV','hydrophobicity_ENGD860101': 'SGTAW',
           'hydrophobicity_FASG890101': 'NTPG','normwaalsvolume': 'NVEQIL','polarity': 'PATGS',
           'polarizability': 'CPNVEQIL','charge': 'ANCQGHILMFPSTWYV', 
           'secondarystruct': 'VIYCWFT', 'solventaccess': 'RKQEND'}
    
    group3 = {'hydrophobicity_PRAM900101': 'CLVIMFW','hydrophobicity_ARGP820101': 'LYPFIW',
           'hydrophobicity_ZIMJ680101': 'LPFYI','hydrophobicity_PONP930101': 'YMFWLCVI',
           'hydrophobicity_CASG920101': 'FIWC','hydrophobicity_ENGD860101': 'CVLIMF',
           'hydrophobicity_FASG890101': 'AYHWVMFLIC','normwaalsvolume': 'MHKFRYW',
           'polarity': 'HQRKNED','polarizability': 'KMHFRYW','charge': 'DE',
           'secondarystruct': 'GNPSD','solventaccess': 'MSPTHY'}
    
    property = ['hydrophobicity_PRAM900101', 'hydrophobicity_ARGP820101', 'hydrophobicity_ZIMJ680101', 'hydrophobicity_PONP930101',
	'hydrophobicity_CASG920101', 'hydrophobicity_ENGD860101', 'hydrophobicity_FASG890101', 'normwaalsvolume',
	'polarity', 'polarizability', 'charge', 'secondarystruct', 'solventaccess']
    
    encoding = []
    aaPair = [sequence[j:j+2] for j in range(len(sequence)-1)]
    
    for p in property:
        c1221, c1331, c2332 = 0, 0, 0
        for pair in aaPair:
            if (pair[0] in group1[p] and pair[1] in group2[p]) or (pair[0] in group2[p] and pair[1] in group1[p]):
                c1221 += 1
                continue
            if (pair[0] in group1[p] and pair[1] in group3[p]) or (pair[0] in group3[p] and pair[1] in group1[p]):
                c1331 += 1
                continue
            if (pair[0] in group2[p] and pair[1] in group3[p]) or (pair[0] in group3[p] and pair[1] in group2[p]):
                c2332 += 1
        encoding.append(c1221/len(aaPair))
        encoding.append(c1331/len(aaPair))
        encoding.append(c2332/len(aaPair))
    
    return encoding


# PROTEIN FEATURE: Z-SCALE
# --------------------------------------------------
def zscale(sequence):
    zdict = {
		'A': [0.24,  -2.32,  0.60, -0.14,  1.30], # A
		'C': [0.84,  -1.67,  3.71,  0.18, -2.65], # C
		'D': [3.98,   0.93,  1.93, -2.46,  0.75], # D
		'E': [3.11,   0.26, -0.11, -0.34, -0.25], # E
		'F': [-4.22,  1.94,  1.06,  0.54, -0.62], # F
		'G': [2.05,  -4.06,  0.36, -0.82, -0.38], # G
		'H': [2.47,   1.95,  0.26,  3.90,  0.09], # H
		'I': [-3.89, -1.73, -1.71, -0.84,  0.26], # I
		'K': [2.29,   0.89, -2.49,  1.49,  0.31], # K
		'L': [-4.28, -1.30, -1.49, -0.72,  0.84], # L
		'M': [-2.85, -0.22,  0.47,  1.94, -0.98], # M
		'N': [3.05,   1.62,  1.04, -1.15,  1.61], # N
		'P': [-1.66,  0.27,  1.84,  0.70,  2.00], # P
		'Q': [1.75,   0.50, -1.44, -1.34,  0.66], # Q
		'R': [3.52,   2.50, -3.50,  1.99, -0.17], # R
		'S': [2.39,  -1.07,  1.15, -1.39,  0.67], # S
		'T': [0.75,  -2.18, -1.12, -1.46, -0.40], # T
		'V': [-2.59, -2.64, -1.54, -0.85, -0.02], # V
		'W': [-4.36,  3.94,  0.59,  3.44, -1.59], # W
		'Y': [-2.54,  2.44,  0.43,  0.04, -1.47], # Y
		'-': [0.00,   0.00,  0.00,  0.00,  0.00], # -
	}

    sequence=sequence.replace('X','-').replace('U','-').replace('B','-').replace('Z','-').replace('*','-')
    z1, z2, z3, z4, z5 = 0, 0, 0, 0, 0
    for aa in sequence:
        z1 += zdict[aa][0]
        z2 += zdict[aa][1]
        z3 += zdict[aa][2]
        z4 += zdict[aa][3]
        z5 += zdict[aa][4]
    encoding = [z1/len(sequence), z2/len(sequence), z3/len(sequence), z4/len(sequence), z5/len(sequence)]
    
    return encoding



if __name__ == '__main__':
    # file output path
    walkfile = walkFile('/bios-store1/home/TongqingWei/phage/phage_external/PHIAF/protein')
    for ls in walkfile:
        if ls[:3] == 'cds':
            res_dir = "/bios-store1/home/TongqingWei/phage/phage_external/PHIAF/protein/" + ls
            records = [r for r in SeqIO.parse(res_dir, "fasta")]
            
            ID = []
            for i in records:
                ID.append(i.id)
            
            seq = []
            for i in records:
                seq.append(''.join(list(i.seq)))
                
            # protein features: CTD & Z-scale & protein_features
            extra_feats = np.zeros((len(seq), 47))

            for i,item in enumerate(seq):
                feature_lst = []
                feature_lst  += CTDC(item)
                feature_lst += CTDT(item)
                feature_lst += zscale(item)
                extra_feats[i,:] = feature_lst
    
            extra_feats_df = pd.DataFrame(extra_feats, columns=['CTDC1', 'CTDC2', 'CTDC3', 'CTDT1', 'CTDT2', 'CTDT3', 
                                     'CTDT4', 'CTDT5', 'CTDT6', 'CTDT7', 'CTDT8', 'CTDT9', 'CTDT10', 'CTDT11', 'CTDT12', 'CTDT13', 
                                     'CTDT14', 'CTDT15', 'CTDT16', 'CTDT17', 'CTDT18', 'CTDT19', 'CTDT20', 'CTDT21', 'CTDT22',
                                     'CTDT23', 'CTDT24', 'CTDT25', 'CTDT26', 'CTDT27', 'CTDT28', 'CTDT29', 'CTDT30', 'CTDT31', 
                                     'CTDT32', 'CTDT33', 'CTDT34', 'CTDT35', 'CTDT36', 'CTDT37', 'CTDT38', 'CTDT39', 'Z1', 'Z2',
                                     'Z3', 'Z4', 'Z5'])    
            
            protein_feats = protein_features(seq)
            features = pd.concat([protein_feats, extra_feats_df], axis=1)                
            features.index = ID
            features.to_csv("/bios-store1/home/TongqingWei/phage/phage_external/PHIAF/protein_feature/" + re.findall(r'\_(.+?)\_(.+?)\.', ls)[0][-1] + '.csv')