import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime

class Article:
    def __init__(self, url):
        response = requests.get(url, headers = {'cookie': 'over18=1;'})
        soup = bs(response.text, 'html.parser')
        header = soup.find_all('span','article-meta-value')

        self.author = header[0].text
        self.board = header[1].text
        self.title = header[2].text
        self.time = datetime.strptime(header[3].text, "%a %b %d %H:%M:%S %Y")
        self.content = self.__GetContent(soup)
        self.push = self.__GetPush(soup)

    def __GetContent(self, soup) -> str:
        content_html = soup.find('div', id='main-content', class_='bbs-screen bbs-content')
        lines = content_html.text.split('\n')
        content = ''
        for line in lines[1:]:
            if (line.strip() == '--'):
                break
            content += line + '\n' 
        return content.strip()
    
    def __GetPush(self, soup) -> list[list[str]]:
        content = soup.find_all('div', class_='push')
        push = [u.text for u in content]
        return push
    
    def find_key_in_title(self, keyw: str) -> bool:
        if keyw in self.title:
            return True
        return False
    
    def find_key_in_content(self, keyw: str) -> bool:
        if keyw in self.content:
            return True
        return False
    
    


if __name__ == '__main__':
    article = Article('https://www.ptt.cc/bbs/C_Chat/M.1710226285.A.19E.html')
    for push in article.push:
        print(push)
    