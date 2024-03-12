import os
import re
import requests
from tqdm import tqdm
from .PttArticle import Article


def download_image_in_article(article: Article) -> None:
    if not article.title:
        title = '沒有標題'
    else:
        title = article.title.replace('/', '_')
    
    os.makedirs(title, exist_ok=True)

    urls = re.findall(r"https?://[^'\"\s]+" , article.content)
    jpg_urls = [url.strip() for url in urls if url.endswith('.jpg') or url.endswith('.jpeg')]
    
    index = 0
    for url in tqdm(jpg_urls, desc = '下載圖片'):
        headers = headers = {'content-type': 'text/html; charset=UTF-8', 
                             'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        img = requests.get(url, headers = headers)
        with open(os.path.join(title, f"圖{index+1}.jpg"), "wb") as file: 
            file.write(img.content)
        index += 1

if __name__ == '__main__':
   pass

