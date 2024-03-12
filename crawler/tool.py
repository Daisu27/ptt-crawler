import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from os.path import basename

def URL(boardname: str) -> str:
    url = 'https://www.ptt.cc/bbs/' + boardname + '/index.html'
    return url 

def FindIndex(url: str) -> int:
        '''
        因為看板除了最新頁是index.html，其他頁都是像index123.html，所以從首頁找上頁網址，從中找到數字
        '''
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        html_tag = soup.find('div', class_ = "btn-group btn-group-paging")
        url_tags = html_tag.find_all('a', class_ = 'btn wide')

        for tag in url_tags:
            if '上頁' in tag.text:
                url = tag['href'].strip()
                basename_ = basename(url)
                match = re.search(r'\d+', basename_)
                if match:
                    index = match.group()
                    return int(index)
                else:
                    raise ValueError('沒有 index')

def PrevPageURL(BillBoard: str, index: int):
        '''
        產生看板前一頁 url
        '''
        while index > 0:
            yield f'https://www.ptt.cc/bbs/{BillBoard}/index{index}.html'
            index -= 1

def IsToday(time: datetime) -> bool:
    now = datetime.now()
    yesterday = now - timedelta(hours = 24)
    return time > yesterday

def CountPush(article)-> dict:
        push_list = article.push
        result = {'推': 0, '→': 0, '噓': 0}
        for push in push_list:
            if '推' in push:
                result['推'] += 1
            elif '→' in push:
                result['→'] += 1
            else:
                result['噓'] += 1
        return result

