import h5py
import os
import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem
import subprocess
import typing


def conf_gen(smi, conf_number, smi_charge):
    m = Chem.MolFromSmiles(smi)
    m = Chem.AddHs(m)
    print(smi)
    params = AllChem.ETKDGv3()
    cids = AllChem.EmbedMultipleConfs(m, numConfs=conf_number, params=params)
    res = AllChem.MMFFOptimizeMoleculeConfs(m,
                                            numThreads=40,
                                            mmffVariant="MMFF94")
    energy_low = min(res)
    label = res.index(energy_low)

    conf_mol = Chem.MolToXYZBlock(m, confId=label)
    del cids
    return conf_mol


def convert_pdb2xyz(filename: str, pdbfolder: str, xyzfolder: str) -> str:
    cmd = [
        'obabel', '-ixyz -opdb', f'{pdbfolder}/{filename}.pdb', '-O',
        f'{xyzfolder}/{filename}.xyz'
    ]    #obabel -ixyz -opdb input.pdb  -O input.xyz


db = h5py.File("testdb.hdf5", "r")

IDs = list(db.keys())

for id in IDs:
    group = db[id]
    pdb_block = ""
    xyz_block = ""


    inchi = group["Standard InChI"][0].decode()

    inchi_key=group["Standard InChIKey"][0].decode()

    # run obabel to generate 3d and confs  
    # pick lowest energy conf to be stored one 
    # move file to ok folder 

    del group

db.close()
