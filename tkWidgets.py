import tkinter as tk
import tkinter.font as tkfont
import webbrowser as wwwbro

class HyperLabel(tk.Label):
    def __init__(self, master, text, color=None, underline=False, url=None):
        super().__init__(master, text=text, cursor="hand1")
        if color:
            self.config(fg=color)
        if underline:
            f = tkfont.Font(self, self.cget("font"))
            f.configure(underline=True)
            self.configure(font=f)
        if url:
            self.onclick_openurl(url)
    def onclick_openurl(self, url):
        openurl = lambda e: wwwbro.open_new(url)
        self.bind("<Button-1>", openurl)

class ScrollableFrame(tk.Frame):
    """
       Make a frame scrollable with scrollbar on the right.
       After adding or removing widgets to the scrollable frame, 
       call the update() method to refresh the scrollable area.
       @idea from https://stackoverflow.com/a/47985165
       I added mouse wheel emulation and refactored some trivial parts.
    """
    __slots__ = ['canvas', 'window_item']
    def configure_mouse_wheel(self):
        "emulate mouse wheel action (tkinter doesn't support it by default)"
        canvas = self.canvas
        def mousewheel(e):
            move = 1 if  e.num == 5 or e.delta < 0 else -1
            canvas.yview_scroll(move, "units")
        canvas.bind_all("<MouseWheel>", mousewheel) # for Windows & Mac OS
        canvas.bind_all("<Button-4>", mousewheel) # for Linux
        canvas.bind_all("<Button-5>", mousewheel) # for Linux
    def __init__(self,master):
        # We can attach Scrollbar only to listboxes, canvases, and text fields.
        scroll = tk.Scrollbar(master, orient='vertical')
        scroll.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        self.canvas = canvas = tk.Canvas(master)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # make canvas scrollable
        canvas.config(yscrollcommand=scroll.set)
        scroll.config(command=canvas.yview)
        canvas.bind('<Configure>', self.__fill_canvas)

        # make frame and attach it to canvas
        super().__init__(master)
        self.window_item = canvas.create_window(0, 0, window=self, anchor=tk.NW)

        # emulate mouse wheel
        self.configure_mouse_wheel()
    def __fill_canvas(self, event):
        "Enlarge the windows item to the cnavas width"
        canvas_width = event.width
        self.canvas.itemconfig(self.window_item, width = canvas_width)
    def update(self):
        "Update the canvas and the scrollregion"
        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.window_item))
    def pack(self, **kw):
        "We should not pack() this object"
        return self
