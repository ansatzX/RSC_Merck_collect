from bs4 import BeautifulSoup
import requests
import re
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
keywords = (
    "Monograph ID",
    "Title",
    "Molecular Formula",
    "Molecular Weight",
    "Percent Composition",
    "Standard InChIKey",
    "Standard InChI"
    "Compound CID"
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

def get_query_key_from_merck_id(id):
    with open(f'pages/{id}.html') as f:
        text =f.read()
    res = parse(text)

    query_keyword =['Title']

    return query_keyword

def pubchem_query_best_match(query_keyword):
    query_url = f'https://pubchem.ncbi.nlm.nih.gov/#query={query_keyword}'
    driver.get(query_url)
    time.sleep(2)
    root = driver.find_element(By.ID,"root")
    best_match = root.find_element(By.ID,"featured-results")
    link_element = best_match.find_element(By.TAG_NAME,"a") 
    compound_url = link_element.get_attribute("href")

    best_match_infos= best_match.text
    Compound_CID = ""
    for line in best_match_infos.split("\n"):
        if line.startswith("Compound CID"):
            Compound_CID = line.split(":")[1].strip()
            break
    sdf_url =f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/{Compound_CID}/record/SDF/?record_type=3d&response_type=save&response_basename=Conformer3D_CID_{Compound_CID}'
    data_url =f'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{Compound_CID}/JSON/?response_type=save&response_basename=compound_CID_{Compound_CID}'
    return (compound_url, sdf_url, data_url)

if __name__ == "__main__":
    
    merck_pages  =os.listdir("pages")
    merck_ids = [  page.split(".")[0] for page in merck_pages]


    for id in merck_ids:
        query_keyword = get_query_key_from_merck_id(id)
        compound_url, sdf_url, data_url = pubchem_query_best_match(query_keyword)

        r = requests.get(sdf_url)
        if r.status_code == 200:
            with open(f'pubchem_sdfs/{id}.sdf', "w") as f:
                f.write(r.text)

        r = requests.get(data_url)
        if r.status_code == 200:
            with open(f'pubchem_datas/{id}.json', "w") as f:
                f.write(r.text)

        with open("pubchem_merck_index.csv", "a") as f:
            f.write(f'{id}, {query_keyword},  {compound_url} '+ "\n")