import io
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
'''
This module allows you to download articles from pikabu.ru
'''

PIKABU_DATE = "https://pikabu.ru/search?d={}&D={}&page={}"
PATH = "data"
FILENAME = "\pikabu{}.html"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/80.0.3987.132 YaBrowser/20.3.1.197 Yowser/2.5 Safari/537.36"
}

if __name__ == "__main__":

    page_range = range(1, 15)
    # date_rage = range(2500, 4482)

    date_rage = range(3512, 4200)

    for d in tqdm(date_rage):
        for p in page_range:
            r = requests.get(PIKABU_DATE.format(d, d, p), headers=headers)
            soup = BeautifulSoup(r.text, "lxml")
            articles = soup.findChildren("article")
            for i, article in enumerate(articles):
                file_name = PATH + FILENAME.format("_{}_{}_{}".format(d, p, i))
                with io.open(file_name, "w", encoding="utf-8") as f:
                    f.write(str(article))
                    f.close()
