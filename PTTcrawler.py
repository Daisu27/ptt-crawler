import requests
import re
from bs4 import BeautifulSoup

class PTTcrawler:
    limited = ['Gossiping', 'Sex']
    def __init__(self, url:str):
        self.url = url
        for billboard in self.limited:
            self.headers = {'cookie': 'over18=1;'}
            break
        else:
            self.headers = None

        try:
            response = requests.get(self.url, headers = self.headers)
        except Exception:
            print('failed connetion: ' + str(Exception))
        else:
            self.soup = BeautifulSoup(response.text, 'html5lib')
    
    def title(self):
        title = self.soup.find('title').text
        pattern = r'\[.*?\] .*?(?=\s+-)'
        match = re.search(pattern, title)
        if match:
            return match.group(0)
        else:
            return "without title"
        
    def content(self):
        content = self.soup.find('div', id='main-content', class_='bbs-screen bbs-content')
        return content.text

        
    



if __name__ == '__main__':
    p = PTTcrawler('https://www.ptt.cc/bbs/Gossiping/M.1708973754.A.76A.html')
    print(p.content())

        



