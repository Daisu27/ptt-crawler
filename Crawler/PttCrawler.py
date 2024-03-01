import requests
import re

from os.path import basename
from HttpRequestManger import HTTPRequestManager
from HtmlParser import HTMLParser
from PttArticle import ArticleInfo_Extractor
from tool import URL

class PttCrawler:    
    def __init__(self, Billboard: str, KeyWord: str = ''):
        self.url = URL(Billboard)
        self.keyw = KeyWord
        self.http_manager = HTTPRequestManager()
        self.html_parser = HTMLParser()
        self.data_extractor = ArticleInfo_Extractor()
        self.articles = []

    def crawl(self):
        request = self.http_manager.Get(self.url)
        soup = self.html_parser.parse(request.text)
        article_urls = self.FindArticlesURL(soup)
        for url in article_urls:
            article_request = self.http_manager.Get(url)
            article_soup = self.html_parser.parse(article_request.text)
            article_info = self.data_extractor.extract_info(article_soup)
            if self.keyw in article_info.title or self.keyw in article_info.content:
                self.articles.append(article_info.title)

    def crawl_result(self) -> list:
        return self.articles
    
    def FindArticlesURL(self, soup) -> dict[str:str]:
        '''
        找尋本頁內的文章網址
        '''
        html_tags = soup.find_all('div', class_ = 'r-ent')
        link_urls = []
        for tag in html_tags:
            link_url = tag.find('div', class_ = 'title').a['href'].strip()
            link_urls.append('https://www.ptt.cc' + link_url)
        return link_urls
    
    def __FindIndex(self, soup) -> str:
        '''
        因為看板除了最新頁是index.html，其他頁都是像index123.html，所以從首頁找上頁網址，從中找到數字
        '''
        html_tag = soup.find('div', class_ = "btn-group btn-group-paging")
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
    p = PttCrawler('Gossiping', '打結')
    p.crawl()
    for _ in p.crawl_result():
        print(_)
