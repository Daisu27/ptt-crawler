import requests
import re
from bs4 import BeautifulSoup

class PttArticle:
    def __init__(self, url:str):
        self.url = url
        self.headers = {'cookie': 'over18=1;'}

        try:
            response = requests.get(self.url, headers = self.headers)
        except Exception:
            print('failed connetion: ' + str(Exception))
        else:
            self.soup = BeautifulSoup(response.text, 'html5lib')
        
        self.title = self.__get_title()
        self.author = self.__get_author()
        self.post_time = self.__get_post_time()
        self.content = self.__get_content()
        self.push = self.__get_push()
    
    def __get_title(self) -> str:
        title = self.soup.find('title').text
        pattern = r'\[.*?\] .*?(?=\s+-)'
        match = re.search(pattern, title)
        if match:
            return match.group(0)
        else:
            return "without title"

    def __get_author(self) -> str:
        author = self.soup.find('span', class_ = 'article-meta-value')
        return author.text

    def __get_post_time(self):
        metalines = self.soup.find_all('div', class_='article-metaline')
        print(metalines)
        for metaline in metalines:
            meta_tag = metaline.find('span', class_='article-meta-tag')
            if meta_tag and meta_tag.text.strip() == '時間':
                time = metaline.find('span', class_='article-meta-value')
        return time.text
        
    def __get_content(self) -> str:
        content = self.soup.find('div', id='main-content', class_='bbs-screen bbs-content')
        return content.text
    
    def __get_push(self) -> list[str]:
        content = self.soup.find_all('div', class_='push')
        return [u.text for u in content]
    
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

if __name__ == '__main__':
    p = PttArticle('https://www.ptt.cc/bbs/Marginalman/M.1707657661.A.48A.html')

        



