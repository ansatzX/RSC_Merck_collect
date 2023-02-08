
from bs4 import BeautifulSoup
import requests
import re
import time

for i in range(1, 12287):
    url = "https://www.rsc.org/Merck-Index/monograph/m%d?q=unauthorize" % (i)
    r = requests.get(url)
    if r.status_code == 200:
        # save to disk
        open("pages/%d.html" % (i), "w").write(r.text)
        print("%d ok" % (i))
    else:
        print("%d fail" % (i))

    time.sleep(2)