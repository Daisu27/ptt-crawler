import re
from datetime import datetime
from .HttpRequestManger import HttpRequestManager
from .HtmlParser import HTMLParser
from dataclasses import dataclass, field

@dataclass
class ArticleInfo:
    title: str = None
    author: str = None
    board: str = None
    time :str= None
    content: str = None
    push: list= field(default_factory=list)
    
class ArticleInfo_Extractor:
    def __call__(self, soup) -> ArticleInfo:
        header = soup.find_all('span','article-meta-value')
        author = header[0].text
        board = header[1].text
        title = header[2].text
        time = datetime.strptime(header[3].text, "%a %b %d %H:%M:%S %Y")
        content = self.__GetContent(soup)
        push = self.__GetPush(soup)
        return ArticleInfo(title, author, board, time, content, push)

    def __GetContent(self, soup) -> str:
        content_html = soup.find('div', id='main-content', class_='bbs-screen bbs-content')
        lines = content_html.text.split('\n')
        content = ''
        for line in lines[1:]:
            if (line.strip() == '--'):
                break
            content += line + '\n' 
        return content.strip()
    
    def __GetPush(self, soup) -> list[str]:
        content = soup.find_all('div', class_='push')
        return [u.text for u in content]

if __name__ == '__main__':
    url = 'https://www.ptt.cc/bbs/Gossiping/M.1684471909.A.07E.html'
    request = HttpRequestManager()
    html = HTMLParser()
    soup = html.parse(request.Get(url).text)
    article = ArticleInfo_Extractor()
    art = article(soup)
    print(art.time)
    