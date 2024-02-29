import re
from dataclasses import dataclass

@dataclass
class ArticleInfo:
    title: str = None
    url: str = None
    author: str = None
    conetent: str = None
    push = []

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
    def extract_info(self, soup) -> tuple[str, str, str, str, str]:
        author = self.__GetAuthor(soup)
        title = self.__GetTitle(soup)
        time = self.__GetPostTime(soup)
        content = self.__GetContent
        push = self.__GetPush(soup)
        return author, title, time
    
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
            return "without title"
    
    def __GetPostTime(self, soup):
        metalines = self.soup.find_all('div', class_='article-metaline')
        print(metalines)
        for metaline in metalines:
            meta_tag = metaline.find('span', class_='article-meta-tag')
            if meta_tag and meta_tag.text.strip() == '時間':
                time = metaline.find('span', class_='article-meta-value')
        return time.text

    def __GetContent(self, soup) -> str:
        content = soup.find('div', id='main-content', class_='bbs-screen bbs-content')
        return content.text
    
    def __GetPush(self, soup) -> list[str]:
        content = soup.find_all('div', class_='push')
        return [u.text for u in content]

if __name__ == '__main__':
    pass

        



