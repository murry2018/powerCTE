import requests
from bs4 import BeautifulSoup as bs
import pickle

class Site:
    __slots__ = ['name', 'url', 'parse', 'soup', 'items', 'uniques']
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
        self.uniques = []
    def set_rule(self, parseRule):
        self.parse = parseRule
    def method(self):
        self.get_page()
        self.get_items()
        res=[]
        try:
            with open(self.name + ".dat", 'rb') as data:
                other_items = pickle.load(data)
                self.uniques = self.diff(other_items)
                if self.uniques == []:
                    res.append(("최신 데이터가 없습니다", self.url))
                else:
                    res = self.uniques
        except FileNotFoundError:
            res = self.items
        with open(self.name + ".dat", 'wb') as data:
            pickle.dump(self.items, data)
        return res
    def get_notunique(self):
        return [item for item in self.items if item not in self.uniques]
    def get_page(self):
        r = requests.get(self.url, headers={'User-agent': 'Mozilla/5.0'})
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
    def diff(self, other_items):
        return [item for item in self.items if item not in other_items]
