
from bs4 import BeautifulSoup
import requests
import re
import time

for i in range(1, 12287):
    url = f'https://www.rsc.org/Merck-Index/monograph/m{i}?q=unauthorize'
    r = requests.get(url)
    if r.status_code == 200:
        # save to disk
        with open(f'pages/{i}.html', "w") as f:
            f.write(r.text)
        print(f'{i} ok')
    else:
        print(f'{i} fail')

    time.sleep(1)