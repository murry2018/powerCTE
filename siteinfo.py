import requests
from bs4 import BeautifulSoup as bs

class Site:
    __slots__ = ['name', 'url', 'parse', 'soup', 'items']
    def __init__(self, name, url, parseRule=None):
        """
           name -- 사이트 이름
           url -- 페이지 주소
           parseRule -- 페이지에서 아이템을 가져오는 규칙
           시그너쳐:: __init__(self, name: str, url: str,
                                parseRule: soup -> List[url])
        """
        self.name = name
        self.url = url
        self.parse = parseRule
        self.soup = None
        self.items = None
    def set_rule(self, parseRule):
        self.parse = parseRule
    def method(self):
        self.get_page()
        return self.get_items()
    def get_page(self):
        r = requests.get(self.url)
        self.soup = bs(r.text, 'html.parser')
        return r.status_code
    def get_items(self, soup=None):
        if self.parse is None:
            raise RuntimeError("There's no parse rule designated.")
        if self.soup is None and soup is None:
            raise RuntimeError("Site.get_page() first")
        if soup is not None:
            if not isinstance(soup, bs):
                raise RuntimeError("Invalid BeautifulSoup object")
            else:
                self.soup = soup
        self.items = self.parse(self.soup)
        return self.items
