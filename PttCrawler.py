import requests
from bs4 import BeautifulSoup
from PttArticle import PttArticle


class PttCrawler:
    def __init__(self, billboard: str = 'Gossiping'):
        self.url = 'https://www.ptt.cc/bbs/' + billboard + '/index.html'
        self.headers = {'cookie': 'over18=1;'}
        self.articles = []
        try:
            response = requests.get(self.url, headers = self.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("HTTP 錯誤:", e)
        except requests.exceptions.Timeout as e:
            print("請求超時:", e)
        except requests.exceptions.ConnectionError as e:
            print("連接錯誤:", e)
        self.soup = BeautifulSoup(response.text, 'html5lib')
    
    def find_articles_url(self) -> list[str]:
        pages = self.soup.find_all('div', class_ = 'r-ent')
        link_urls = []
        for page in pages:
            link_url = page.find('div', class_='title').a['href'].strip()
            link_urls.append('https://www.ptt.cc' + link_url)
        return link_urls
    
    def find_next_page(self):
        pass

if __name__ == '__main__':
    p = PttCrawler('C_Chat')
    print(p.find_articles_url())
