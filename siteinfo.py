import requests
from bs4 import BeautifulSoup
import pickle

class SiteInfo:
    def __init__(self, name, url, rule=None, req_method='get', data=None):
        """Object Initializing
        name -- site's name
        url -- page's url
        rule -- scraping rule to extract items from page
                (given BeautifulSoup object, produce list of items)
        req_method -- get or post
        data -- additional GET parameter or POST data
        """
        (self.name, self.url, self.rule, self.req_method, self.data) = (
            name, url, rule, req_method, data)
        # dictionary of options to easily configure object options
        self.options = {
            'name': self.name,
            'url': self.url,
            'rule': self.rule,
            'req_method': self.req_method,
            'data': self.data }
        # Intermediate prodcuts: soup, items
        (self.soup, self.items, self.olddata) = (None, None, None)
    def config(self, **opts):
        """Configure SiteInfo object's options
        **opts -- pairs of option name - value 
        Options can be name, url, rule, req_method, or data.
        """
        for name, value in opts.items():
            try: self.options.get(key)
            except KeyError:
                raise ValueError("config: Option should be in " +
                        "['name', 'url', 'rule', 'req_method', 'data']")
            self.options[name] = value
    def getPage(self):
        """Get page from remote source
        """
        resp = None
        if self.req_method == 'post':
            resp = requests.post(self.url, data=self.data)
        else: # req_method = 'get'
            resp = requests.get(self.url, params=self.data)
        self.soup = BeautifulSoup(resp.text, 'html.parser')
        return resp.status_code
    def getItems(self, page=None):
        """Extract items from page
        Recommend: SiteInfo.getPage() first
        page -- alternative html page to result of getPage()
        """
        if self.soup is None and page is None:
            raise ValueError("No page designated. Try SiteInfo.getPage()")
        if self.rule is None:
            raise ValueError("No parse rule designated. " +
                    "SiteInfo.config(rule=<parse rule>) to set parse rule.")
        soup = self.soup
        if page is not None:
            soup = BeautifulSoup(page, 'html.parser')
        self.items = self.rule(soup)
        return self.items
    def getRefreshedItems(self):
        """Refresh items and produce those items.
        """
        self.getPage()
        return self.getItems()
    def loadData(self, filename=None):
        """Load past pickled data (page items); produce nothing
        """
        if filename is None:
            filename = self.name + ".dat"
        try:
            with open(filename, 'rb') as data:
                self.olddata = pickle.load(data)
        except FileNotFoundError:
            self.olddata = []
    def collectLatestItems(self):
        """Collect latest items (But we should Siteinfo.getItems() first.)
        """
        return [item for item in self.items if item not in self.olddata]
    def collectCommonItems(self):
        """Collect common items (But we should Siteinfo.getItems() first.)
        """
        return [item for item in self.items if item in self.olddata]
    def saveData(self, filename=None):
        """pickle and dump current data (page items)
        """
        if filename is None:
            filename = self.name + ".dat"
        with open(filename, 'wb') as data:
            pickle.dump(self.items, data)
