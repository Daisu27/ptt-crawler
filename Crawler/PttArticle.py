import re
from HttpRequestManger import HTTPRequestManager
from HtmlParser import HTMLParser
from dataclasses import dataclass, field

@dataclass
class ArticleInfo:
    title: str = None
    url: str = None
    author: str = None
    time :str= None
    content: str = None
    push: list= field(default_factory=list)

    def count_push(self)-> dict:
        push_list = self.push
        result = {'推': 0, '→': 0, '噓': 0}
        for push in push_list:
            if '推' in push:
                result['推'] += 1
            elif '→' in push:
                result['→'] += 1
            else:
                result['噓'] += 1
        return result
    
class ArticleInfo_Extractor:
    def extract_info(self, soup) -> ArticleInfo:
        author = self.__GetAuthor(soup)
        title = self.__GetTitle(soup)
        url = self.__GetPageURL(soup)
        time = self.__GetPostTime(soup)
        content = self.__GetContent(soup)
        push = self.__GetPush(soup)
        return ArticleInfo(title, url, author, time, content, push)
    
    def __GetAuthor(self,soup) -> str:
        author = soup.find('span', class_ = 'article-meta-value')
        return author.text

    def __GetTitle(self, soup) -> str:
        title = soup.find('title').text
        pattern = r'\[.*?\] .*?(?=\s+-)'
        match = re.search(pattern, title)
        if match:
            return match.group(0)
        else:
            return "沒有標題"
    
    def __GetPageURL(self, soup):
        url = None
        url_tags = soup.find_all('span', class_='f2')
        for tag in url_tags:
            if  tag is not None and '※ 文章網址: ' in tag.text:
                link_tag = tag.find('a')
                if link_tag:
                    url = link_tag['href']
                    break
        return url

    def __GetPostTime(self, soup):
        metalines = soup.find_all('div', class_='article-metaline')
        for metaline in metalines:
            meta_tag = metaline.find('span', class_='article-meta-tag')
            if meta_tag and meta_tag.text.strip() == '時間':
                time = metaline.find('span', class_='article-meta-value')
        return time.text

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
    url = 'https://www.ptt.cc/bbs/Gossiping/M.1709271710.A.20E.html'
    request = HTTPRequestManager()
    html = HTMLParser()
    soup = html.parse(request.Get(url).text)
    article = ArticleInfo_Extractor().extract_info(soup)
    print(article.content)
    