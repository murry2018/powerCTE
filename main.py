#-*- coding: utf-8 -*-

## powerCTE Version proto.1
## If there is unicode issue, please use latest version of python.
import requests
from bs4 import BeautifulSoup as bs

class Site:
    def __init__(self, url, parseRule):
        self.url = url
        self.parse = parseRule

def rule_wlibfacebook(Soup):
    mainContents = Soup.find('div', {'role':'main'})
    v = zip(mainContents.select('div.userContent'),
            mainContents.select('span.timestampContent'))
    for userContent, timestamp in v:
        print(timestamp.contents[0], end=':: ')
        print(userContent.select('p')[0].contents[0].strip())

def rule_ityonsei(soup):
    titles = map(lambda s: s.find('a').contents[0].strip(),
                 soup.select('td.title'))
    when = map(lambda s: s.contents[0].strip(),
               soup.select('td.time'))
    v = zip(titles, when)
    for title, timestamp in v:
        print(timestamp, end=':: ')
        print(title)

def rule_yonsei(soup):
    mainContents = soup.select('ul.board_list')[0].findAll('li')
    for content in mainContents:
        if 'class' not in content.attrs:
            title = content.find('strong').text.replace('만료','').strip()
        else:
            title = "NOTICE: "
            title += content.find('strong').text.replace("[공지]", "").strip()
        when = content.select('span.tline')[1].text.strip()
        print(when, end=':: ')
        print(title)
        
urls = ["http://it.yonsei.ac.kr/index.php?mid=board_notice",
        "http://www.yonsei.ac.kr/wj/support/notice.jsp",
        "https://www.facebook.com/pg/ysbookmark/posts/?ref=page_internal"]

sites = []
sites.append(Site(urls[0], rule_ityonsei))
sites.append(Site(urls[1], rule_yonsei))
sites.append(Site(urls[2], rule_wlibfacebook))

print("[PowerCTE proto.1]")

for site in sites:
    print("\nNow traveling ", site.url, " ...")
    r = requests.get(site.url)
    print("Status:",r.status_code)
    print("Coding:",r.encoding)
    input("Show contnets? [Press Enter]")
    soup = bs(r.text, features="html.parser")
    site.parse(soup)
