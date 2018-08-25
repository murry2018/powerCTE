#-*- coding: utf-8 -*-
from ui import *
import siteinfo as site

# 연세대학교
def rule_yonsei(soup):
    items = []
    mainContents = soup.select('ul.board_list')[0].findAll('li')
    for content in mainContents:
        if 'class' not in content.attrs:
            title = content.find('strong').text.replace('만료','').strip()
        else:
            title = "NOTICE: "
            title += content.find('strong').text.replace("[공지]", "").strip()
        when = content.select('span.tline')[1].text.strip()
        items.append((when+':: '+title, "http://www.yonsei.ac.kr/wj/support/notice.jsp"))
    return items

# 컴퓨터정보통신공학부
def rule_ityonsei(soup):
    items = []
    titles = map(lambda s: s.find('a').contents[0].strip(),
                 soup.select('td.title'))
    when = map(lambda s: s.contents[0].strip(),
               soup.select('td.time'))
    v = zip(titles, when)
    for title, timestamp in v:
        items.append((timestamp+':: '+title, "http://it.yonsei.ac.kr/index.php?mid=board_notice"))
    return items

# 원주학술정보센터자치회
def rule_wlibfacebook(Soup):
    items = []
    mainContents = Soup.find('div', {'role':'main'})
    v = zip(mainContents.select('div.userContent'),
            mainContents.select('span.timestampContent'))
    for userContent, timestamp in v:
        when = timestamp.contents[0]
        title = userContent.select('p')[0].contents[0].strip()
        items.append((when+':: '+title, "http://it.yonsei.ac.kr/index.php?mid=board_notice"))
    return items

app = myApp()
sites = [
    site.Site("연세대학교",
              "http://www.yonsei.ac.kr/wj/support/notice.jsp",
              rule_yonsei),
    site.Site("컴퓨터정보통신공학부",
              "http://it.yonsei.ac.kr/index.php?mid=board_notice",
              rule_ityonsei),
    site.Site("원주학술정보센터 자치회 책갈피",
              "https://www.facebook.com/pg/ysbookmark/posts/?ref=page_internal",
              rule_wlibfacebook)
    ]       
for site in sites:
    app.add_site(site)
app.run()
