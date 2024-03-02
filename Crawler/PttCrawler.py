import time

from HttpRequestManger import HTTPRequestManager
from HtmlParser import HTMLParser
from PttArticle import ArticleInfo_Extractor
from tool import URL, FindIndex, PrevPageURL

class PttCrawler:    
    def __init__(self):
        self.http_manager = HTTPRequestManager()
        self.html_parser = HTMLParser()
        self.data_extractor = ArticleInfo_Extractor()
        self.articles = []

    def crawl(self, BillBoard: str, keyw: str, n: int = 0):
        url = URL(BillBoard)
        request = self.http_manager.Get(url)
        soup = self.html_parser.parse(request.text)
        article_urls = self.FindArticlesURL(soup)

        self.Find(article_urls, keyw) # 爬取首頁
        time.sleep(10)
        index = FindIndex(soup)
        i = index
        url_gen = PrevPageURL(BillBoard, index)

        while i > (index - n):
            url = next(url_gen)
            request = self.http_manager.Get(url)
            soup = self.html_parser.parse(request.text)
            article_urls = self.FindArticlesURL(soup)
            self.Find(article_urls, keyw)
            i -= 1
    
    def Find(self,URLlist: list, keyw :str):
        for url in URLlist:
            article_request = self.http_manager.Get(url)
            article_soup = self.html_parser.parse(article_request.text)
            article_info = self.data_extractor.extract_info(article_soup)
            if keyw in article_info.title or keyw in article_info.content:
                self.articles.append(article_info.title)

    def crawl_result(self) -> list:
        return self.articles
    
    def FindArticlesURL(self, soup) -> list[str]:
        '''
        找尋本頁內的文章網址
        '''
        html_tags = soup.find_all('div', class_ = 'r-ent')
        link_urls = []
        for tag in html_tags:
            title_tag = tag.find('div', class_='title')
            if title_tag is not None:
                link_tag = title_tag.find('a')  # 尋找包含連結的 a 標籤
                if link_tag is not None:
                    link_url = link_tag['href'].strip()
                    link_urls.append('https://www.ptt.cc' + link_url)
        return link_urls

if __name__ == '__main__':
    p = PttCrawler()
    p.crawl('Gossiping', '臭', 5)
    
    for _ in p.crawl_result():
        print(_)
