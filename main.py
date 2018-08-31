#-*- coding: utf-8 -*-
from ui import *
import mysites
from functools import partial
app = DefaultApp()
for site in mysites.sites:
    def item_rule(site):
        site.getRefreshedItems()
        site.loadData()
        site.saveData()
        return site.collectLatestItems()
    method = partial(item_rule, site)
    app.add_site(site.name, site.url, method, site.collectCommonItems)
app.run()
