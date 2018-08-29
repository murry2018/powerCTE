#-*- coding: utf-8 -*-
import tkinter as tk
import tkWidgets as tkw # tkWidgets.py

class ItemHolder:
    __slots__ = ['sitewidget', 'items']
    def __init__(self, sitewidget, items):
        self.sitewidget = sitewidget
        self.items = items

class TitleBar(tk.Frame):
    more_text = "펼치기"
    hide_text = "숨기기"
    __slots__ = ['label_title', 'button_more']
    def __init__(self, parent, name, url):
        super().__init__(parent)
        # Title
        self.label_title = title = tkw.HyperLabel(self, name, url=url)
        title.pack(side=tk.LEFT, anchor='w')
        # 'More' Button
        self.button_more = button_more = tk.Button(self, text=TitleBar.more_text)
        button_more.pack(side=tk.RIGHT, anchor='e')
    def title(self, text):
        self.title.config(text=text)
    def on_button_more_click(self, func):
        self.button_more.config(command=func)

class ItemPanel(tk.Frame):
    load_text = "불러오기"
    loading_text = "로딩 중..."
    __slots__ = ['button_load', '_open']
    def __init__(self, parent):
        super().__init__(parent)
        self.button_load = tk.Button(self, text=ItemPanel.load_text)
        self.button_load.pack()
        self._open = False
    def add_page(self, name, url):
        tkw.HyperLabel(self, name, color="blue",
                       underline=True, url=url).pack()
    def on_button_load_click(self, func):
        self.button_load.config(command=func)
    def is_open(self):
        return self._open

class SiteWidget(tk.Frame):
    __slots__ = ['titlebar', 'itempanel']
    def __init__(self, parent, name, url):
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1) # expand child item's width
        # TitleBar
        self.titlebar = TitleBar(self, name, url)
        self.titlebar.grid(row=0, sticky='we')
        # Item panel; This is hidden at the first time.
        self.itempanel = ItemPanel(self)
    def hide_panel(self):
        self.itempanel.grid_forget()
        self.itempanel._open = False
    def show_panel(self):
        self.itempanel.grid(row=1, sticky='we')
        self.itempanel._open = True
        
from functools import partial
import threading

class DefaultApp:
    app_name = "공지 모아보기"
    def __init__(self, winfo=(800,600,100,100), title=None):
        self.master = master = tk.Tk()
        master.wm_geometry("%dx%d+%d+%d" % winfo)
        if title is None: title = DefaultApp.app_name
        master.title(title)
        self.container = tkw.ScrollableFrame(master)
        self.sites = []
    def add_site(self, name, url, method):
        # Site widget
        newsite = SiteWidget(self.container, name, url)
        self.sites.append(newsite)
        newsite.pack(fill=tk.X)
        self.container.update()
        # SiteWidget.TitleBar.button_more handler
        button_more_handler = partial(self.more_item, newsite)
        newsite.titlebar.on_button_more_click(button_more_handler)
        # SiteWidget.ItemPanel.button_load handler
        dataholder = ItemHolder(sitewidget=newsite, items=[])
        button_load_handler = partial(self.load_item, name, method, dataholder)
        newsite.itempanel.on_button_load_click(button_load_handler)
        # SiteWidget.ItemPanel.button_load <<LoadDone>> handler
        loaddone_handler = partial(self.load_done, dataholder)
        newsite.bind("<<LoadDone>>", loaddone_handler)
    def more_item(self, sitewidget):
        """ EventHandler for SiteWidget.TitleBar.button_more """
        if sitewidget.itempanel.is_open():
            sitewidget.hide_panel()
            sitewidget.titlebar.button_more.config(text=TitleBar.more_text)
        else:
            sitewidget.show_panel()
            sitewidget.titlebar.button_more.config(text=TitleBar.hide_text)
        self.container.update()
    def load_item(self, name, method, dataholder):
        """ Event handler for SiteWidget.ItemPanel.button_load """
        "`dataholder' holds sitewidget and list of items"
        def load(name, method):
            dataholder.items = method()
            print("LoadDone")
            dataholder.sitewidget.event_generate('<<LoadDone>>', when='tail')
        panel = dataholder.sitewidget.itempanel
        panel.button_load.pack_forget()
        panel.button_load = tk.Label(panel, text=ItemPanel.loading_text)
        panel.button_load.pack()
        thread = threading.Thread(target=load, args=(name, method))
        thread.start()
    def load_done(self, dataholder, e):
        """ Event handler for SiteWidget.ItemPanel.button_load <<LoadDone>>
            This handler controls app UI """
        panel = dataholder.sitewidget.itempanel
        panel.button_load.pack_forget()
        for name, url in dataholder.items:
            tkw.HyperLabel(panel, name, url=url,
                           color="blue", underline=True).pack()
        self.container.update()
    def run(self):
        self.master.mainloop()
