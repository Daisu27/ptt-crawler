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
    
    def title(self) -> str:
        title = self.soup.find('title').text
        pattern = r'\[.*?\] .*?(?=\s+-)'
        match = re.search(pattern, title)
        if match:
            return match.group(0)
        else:
            return "without title"
        
    def content(self) -> str:
        content = self.soup.find('div', id='main-content', class_='bbs-screen bbs-content')
        return content.text
    
    def get_push(self) -> list[str]:
        content = self.soup.find_all('div', class_='push')
        return [u.text for u in content]
    
    def count_push(self)-> dict:
        push_list = self.get_push()
        result = {'推': 0, '→': 0, '噓': 0}
        for push in push_list:
            if '推' in push:
                result['推'] += 1
            elif '→' in push:
                result['→'] += 1
            else:
                result['噓'] += 1
        return result

if __name__ == '__main__':
    p = PTTcrawler('https://www.ptt.cc/bbs/Marginalman/M.1707657661.A.48A.html')
    print(p.count_push())

        



