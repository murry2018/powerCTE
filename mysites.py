from siteinfo import SiteInfo

# 연세대학교
def rule_yonsei(soup):
    items = []
    url = "http://www.yonsei.ac.kr/wj/support/notice.jsp"
    mainContents = soup.select('ul.board_list')[0].findAll('li')
    for content in mainContents:
        title = content.find('strong').text
        if 'class' not in content.attrs: # 일반적인 공지사항
            title = title.replace('만료','').strip()
        else: # 주요 공지사항
            title = "NOTICE: " + title.replace("[공지]", "").strip()
        when = content.select('span.tline')[1].text.strip()
        items.append((when+':: '+title, url))
    return items

# 컴퓨터정보통신공학부
def rule_ityonsei(soup):
    items = []
    url = "http://it.yonsei.ac.kr/index.php?mid=board_notice"
    titles = map(lambda s: s.find('a').contents[0].strip(),
                 soup.select('td.title'))
    when = map(lambda s: s.contents[0].strip(),
               soup.select('td.time'))
    v = zip(titles, when)
    for title, timestamp in v:
        items.append((timestamp+':: '+title, url))
    return items

# 원주학술정보센터자치회
def rule_wlibfacebook(Soup):
    items = []
    url = "https://www.facebook.com/pg/ysbookmark/posts/?ref=page_internal"
    mainContents = Soup.find('div', {'role':'main'})
    v = zip(mainContents.select('div.userContent'),
            mainContents.select('span.timestampContent'))
    for userContent, timestamp in v:
        when = timestamp.contents[0]
        title = userContent.select('p')
        if title == []:
            title = "(텍스트가 없는 소식)"
        else :
            title = title[0].contents[0].strip()
        items.append((when+':: '+title, url))
    return items

sites = [
    SiteInfo("연세대학교",
             "http://www.yonsei.ac.kr/wj/support/notice.jsp",
             rule=rule_yonsei),
    SiteInfo("컴퓨터정보통신공학부",
             "http://it.yonsei.ac.kr/index.php?mid=board_notice",
             rule=rule_ityonsei),
    SiteInfo("원주학술정보센터 자치회 책갈피",
             "https://www.facebook.com/pg/ysbookmark/posts/?ref=page_internal",
             rule=rule_wlibfacebook)
    ]
