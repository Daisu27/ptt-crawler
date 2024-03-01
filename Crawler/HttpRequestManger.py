import requests

class HTTPRequestManager:
    def __init__(self, headers = None):
        self.session = requests.Session()
        if headers is None:
            self.headers = {'cookie': 'over18=1;'}
        else:
            self.headers = headers
        self.session.headers.update(self.headers)

    def Get(self, url):
        try:
            response = self.session.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print('HTTP 錯誤: ', e)
        except requests.exceptions.Timeout as e:
            print('請求超時: ', e)
        except requests.exceptions.ConnectionError as e:
            print('連接錯誤: ', e)  
        return response
    
    def ResetHeader(self, headers = None):
        self.session.headers.update(headers)


if __name__ == '__main__':
    pass