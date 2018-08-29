#-*- coding: utf-8 -*-
from ui import *
import mysites

app = DefaultApp()
for site in mysites.sites:
    app.add_site(site.name, site.url, site.method)
app.run()
