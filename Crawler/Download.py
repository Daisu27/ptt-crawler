import os
import re
import requests
import time
from tqdm import tqdm
from .PttArticle import ArticleInfo


def Download(Article: ArticleInfo) -> None:
    if not os.path.exists(Article.title):
        os.mkdir(Article.title)

    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', Article.content)
    jpg_urls = [url for url in urls if url.endswith('.jpg') or url.endswith('.jpeg')]
        
    index = 0
    for url in tqdm(jpg_urls, desc = '下載圖片'):
        img = requests.get(url)
        with open(os.path.join(Article.title, f"{index+1}.jpg"), "wb") as file: 
            file.write(img.content)
        index += 1

if __name__ == '__main__':
   pass

