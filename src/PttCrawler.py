import requests
import re

from os.path import basename
from bs4 import BeautifulSoup
from src.PttArticle import PttArticle


class PttCrawler:
    def __init__(self, billboard: str = 'Gossiping'):
        self.url = 'https://www.ptt.cc/bbs/' + billboard + '/index.html'
        self.billboard = billboard
        self.articles = []
        
        self.soup = BeautifulSoup(response.text, 'html5lib')
    
    def find_articles_url(self) -> list[str]:
        '''
        找尋本頁內的文章的url
        '''
        html_tags = self.soup.find_all('div', class_ = 'r-ent')
        link_urls = []
        for tag in html_tags:
            link_url = tag.find('div', class_ = 'title').a['href'].strip()
            link_urls.append('https://www.ptt.cc' + link_url)
        return link_urls
    
    def find_index(self) -> str:
        '''
        因為看板除了最新頁是index.html，其他頁都是像index123.html，所以從首頁找上頁網址，從中找到數字
        '''
        html_tag = self.soup.find('div', class_ = "btn-group btn-group-paging")
        url_tags = html_tag.find_all('a', class_ = 'btn wide')
        for tag in url_tags:
            if '上頁' in tag.text:
                url = tag['href'].strip()
                basename_ = basename(url)
                match = re.search(r'\d+', basename_)
                if match:
                    index = match.group()
                    return index
                else:
                    raise ValueError('沒有 index')

    def page_url(self, n: int) -> str:
        '''
        產生看板前 n 頁的 url
        '''
        index = int(self.find_index())
        while n > 0:
            yield f'https://www.ptt.cc/bbs/{self.billboard}/index{index}.html'
            index -= 1
            n -= 1




if __name__ == '__main__':
    p = PttCrawler()
    url_gen = p.page_url(10)
    try:
        while True:
            print(next(url_gen))
    except:
        pass
