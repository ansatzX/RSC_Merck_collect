from bs4 import BeautifulSoup
import re
import os
import h5py

string = h5py.string_dtype(encoding='utf-8')
keywords = (
    "Monograph ID",
    "Title",
    "Molecular Formula",
    "Molecular Weight",
    "Percent Composition",
    "Standard InChIKey",
    "Standard InChI",
)
    
def parse(html_text):
    res = []
    soup = BeautifulSoup(html_text, features="lxml")
    strongs = soup.find_all("strong")
    for strong in strongs:
        parent = ""
        if str(strong.string) == 'CAS number:' :
            parent = strong.parent

        if len(parent) != 0:
            cas_number_text = str(parent.text)
            cas_number = cas_number_text.split(":")[1].strip()
            res.append(cas_number)

    
    return res
    
def store_dat2h5(id, data, handler):

    group = handler.create_group(str(id))
    for i in range(len(data)):
        # dims = len(data[key])
        dat = data[i]
        group.create_dataset(str(i), dtype=string, shape=(1))[...] = dat

if __name__ == "__main__":
    folder = "./merck_chm_7z_pages"
    files = os.listdir(folder)
    compounds = []
    reactions = []
    for htm in files:
        if len(htm) == 7:
            reactions.append(htm)
        else:
            compounds.append(htm)
    handler = h5py.File("merck_db.hdf5", "w")
    for i in range(len(compounds)):
        drug = os.path.join(folder, compounds[i])
        with open(drug) as f:
            text = f.read()
        res = parse(text)
        if len(res) != 0 :
            store_dat2h5(compounds[i], res, handler)
            print("Done on "+str(i))

    handler.close()