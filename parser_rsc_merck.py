from bs4 import BeautifulSoup
import re
import pandas as pd
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
    
def parse(text):
    soup = BeautifulSoup(text, features="lxml")
    text = soup.get_text()
    
    state = 0
    res = {}
    for line in text.split("\n"):
        if state == 0:
            pattern = "|".join(["^" + k + ":" for k in keywords])
            pattern = re.compile(pattern)
            m = re.match(pattern, line)
            if m:
                state = 1
                keyword = m.group().strip(":")
        elif state == 1:
            if line.strip():
                res[keyword] = line.strip()
                state = 0
    
    return res
    
def store_dat2h5(id, data, handler):

    group = handler.create_group(str(id))
    for key in data.keys():
        # dims = len(data[key])
        group.create_dataset(key, dtype=string, shape=(1))[...] = data[key]

df = pd.DataFrame(columns=keywords)
handler = h5py.File("testdb.hdf5", "w")
for i in range(1, 12287):
    text = open("pages/%d.html" % (i)).read()
    res = parse(text)
    if "Standard InChIKey" in res.keys():
        store_dat2h5(i, res, handler)
        print("Done on "+str(i))

handler.close()