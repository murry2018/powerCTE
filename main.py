#-*- coding: utf-8 -*-
from ui import *
import mysites
from functools import partial
app = DefaultApp()
for site in mysites.sites:
    app.add_site(site)
app.run()
