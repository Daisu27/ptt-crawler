from Crawler.PttCrawler import PttCrawler

def main():
    p = PttCrawler()
    p.crawl('C_Chat', '錢', 5)
    
    for _ in p.crawl_result():
        print(_.title)

if __name__ == '__main__':
    main()
    