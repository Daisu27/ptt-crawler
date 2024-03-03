import time
import sys
from tqdm import tqdm
from .HttpRequestManger import HttpRequestManager
from .HtmlParser import HTMLParser
from .PttArticle import ArticleInfo_Extractor
from .tool import URL, FindIndex, PrevPageURL, IsToday

class PttCrawler:    
    def __init__(self):
        self.http_manager = HttpRequestManager()
        self.html_parser = HTMLParser()
        self.data_extractor = ArticleInfo_Extractor()
        self.articles = []

    def crawl(self, Board: str, keyw: str, n: int = 0):
        '''
        爬取某看板最新n頁內容
        '''
        url = URL(Board)
        print(url)
        article_urls = self.GetArticleURLs(url)

        self.Find(article_urls, keyw) # 爬取首頁
        time.sleep(3)
        
        index = FindIndex(url)
        print(index)
        if index:
            i = index
            url_gen = PrevPageURL(Board, index)

            while i > (index - n):
                try:
                    url = next(url_gen)
                except:
                    sys.exit()

                print(url)
                article_urls = self.GetArticleURLs(url)
                self.Find(article_urls, keyw)
                time.sleep(3)
                i -= 1
    
    def GetArticleURLs(self, url) -> list:
        """
        從給定的 URL 獲取本頁文章鏈接列表
        """
        def FindArticlesURL(soup) -> list[str]:
            '''
            找尋本頁內的文章網址
            '''
            link_urls = []
            title_tags = soup.select('div.r-ent div.title a')
            for tag in title_tags:
                link_url = tag.get('href').strip()
                link_urls.append('https://www.ptt.cc' + link_url)
            return link_urls
        
        request = self.http_manager.Get(url)
        soup = self.html_parser.parse(request.text)
        return FindArticlesURL(soup)

    
    def Find(self,URLlist: list, keyw :str, isToday = True):
        '''
        傳入一個URLlist，從文章標題與文章內容找尋有無要找的關鍵字
        '''
        for url in tqdm(URLlist, desc="查詢此頁文章"):
            request = self.http_manager.Get(url)
            article_soup= self.html_parser.parse(request.text)
            article_info = self.data_extractor(article_soup)
            if isToday:
                if not IsToday(article_info.time):
                    continue
            if keyw in article_info.title or keyw in article_info.content:
                self.articles.append(article_info)

    def crawl_result(self) -> list:
        '''
        回傳抓到的文章
        '''
        return self.articles

if __name__ == '__main__':
    pass