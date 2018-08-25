#-*- coding: utf-8 -*-
from ui import *
import mysites

app = myApp()
for site in mysites.sites:
    app.add_site(site)
app.run()
