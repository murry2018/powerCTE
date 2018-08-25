#-*- coding: utf-8 -*-
import tkinter as tk
import tkWidgets as tkw # tkWidgets.py
class TitleBar(tk.Frame):
    __slots__=['openbutton']
    def __init__(self, master, siteinfo):
        super().__init__(master)
        l = tkw.HyperLabel(self, text=siteinfo.name)
        l.pack(side=tk.LEFT, anchor='w')
        l.onclick_openurl(siteinfo.url)
        self.openbutton = b = tk.Button(self, text="펼치기")
        b.pack(side=tk.RIGHT, anchor='e')

class SiteWidget(tk.Frame):
    __slots__ = ['titlebar','itempanel', 'loadbutton', 'openbutton', 'opened', 'items']
    def __init__(self, master, siteinfo):
        super().__init__(master)
        self.grid_columnconfigure(0,weight=1)
        self.titlebar = titlebar = TitleBar(self, siteinfo)
        titlebar.grid(row=0, sticky='we')
        self.openbutton = titlebar.openbutton
        self.opened = False
        self.itempanel = itempanel = tk.Frame(self)
        self.loadbutton = tk.Button(itempanel, text="가져오기")
        self.loadbutton.pack()
        self.itesm = None
    def hide_items(self):
        self.itempanel.grid_forget()
    def show_items(self):
        self.itempanel.grid(row=1, sticky='we')

import threading
class myApp:
    def __init__(self, winfo=(800,600,100,100), title="공지모아보기"):
        self.root = root = tk.Tk()
        root.title(title)
        root.wm_geometry("%dx%d+%d+%d" % winfo)
        self.container = container = tkw.ScrollableFrame(root)
    def add_site(self, siteinfo):
        s = SiteWidget(self.container, siteinfo)
        s.pack(fill=tk.X)
        def onopenclick(e):
            if s.opened:
                s.hide_items()
                s.openbutton.config(text="펼치기")
            else:
                s.show_items()
                s.openbutton.config(text="숨기기")
            s.opened = not s.opened
            self.container.update()
        s.openbutton.bind("<Button-1>", onopenclick)
        def onloadclick(e):
            def runnnnnnnnnner(siteinfo):
                siteinfo.get_page()
                siteinfo.get_items()
                s.items = siteinfo.items
                print("LoadDone")
                s.event_generate("<<LoadDone>>", when="tail")
            s.loadbutton.pack_forget()
            s.loadbutton = tk.Label(s.itempanel, text="로딩중...")
            s.loadbutton.pack()
            t1 = threading.Thread(target=runnnnnnnnnner, args=(siteinfo,))
            t1.start()
        s.loadbutton.bind("<Button-1>", onloadclick)
        def onloaddone(e):
            s.loadbutton.pack_forget()
            for name, url in s.items:
                h = tkw.HyperLabel(s.itempanel, name, "blue", True)
                h.onclick_openurl(url)
                h.pack()
            self.container.update()
        s.bind("<<LoadDone>>", onloaddone)
        self.container.update()
    def run(self):
        self.root.mainloop()
