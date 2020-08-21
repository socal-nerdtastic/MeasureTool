#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   Documentation is like sex.
#   When it's good, it's very good.
#   When it's bad, it's better than nothing.
#   When it lies to you, it may be a while before you realize something's wrong.
#
# TODO: Add scroll bars or zoom to image view for large images.

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk

SIZE = "800x500" # window start size and position

class GUI(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.refs = []
        self.start = None
        self.current = ''
        self.image = None

        topframe = tk.Frame(self)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        topframe.grid(columnspan=2, sticky='ew')
        btn = ttk.Button(topframe, text='Clear & Load', command=self.load)
        btn.pack(side=tk.LEFT)
        self.filename_lbl = tk.Label(topframe)
        self.filename_lbl.pack(side=tk.LEFT)
        self.c = tk.Canvas(self, bg='white')
        self.c.grid(sticky='nsew', rowspan=2)
        self.c.bind("<Button>", self.on_click)
        self.c.bind("<ButtonRelease>", self.on_release)
        self.c.bind("<Motion>", self.on_motion)
        self.output = ScrolledText(self, width=22)
        self.output.grid(row=1, column=1, sticky='ns')
        self.output.insert(0.0,'X0,Y0,X1,Y1,length\n')
        # ~ btn = ttk.Button(self, text='Clear', command=self.clear)
        # ~ btn.grid(row=2, column=1)
        self.clear()

    def on_click(self, event):
        self.start = event.x, event.y
        self.current = self.c.create_line(*self.start, *self.start, fill='red', width=2)
        self.refs.append(self.current)

    def on_motion(self, event):
        if self.current:
            self.c.coords(self.current, *self.start, event.x, event.y)

    def on_release(self, event):
        self.c.coords(self.current, *self.start, event.x, event.y)
        length = int(((self.start[0]-event.x)**2  + (self.start[1]-event.y)**2)**0.5)
        data = map(str, self.start+(event.x, event.y,length))
        self.output.insert(tk.END,','.join(data)+'\n')
        self.c.coords(self.current, *self.start, event.x, event.y)
        self.current = None

    def clear(self):
        self.output.delete(0.0, tk.END)
        self.output.insert(0.0,'X0,Y0,X1,Y1,length\n')
        while self.refs:
            self.c.delete(self.refs.pop())

    def load(self):
        fn = askopenfilename(filetypes = (("image files",("*.png", "*.jpg")),("all files","*.*")))
        if not fn: return # user cancelled
        self.clear()
        self.filename_lbl.config(text=fn)
        self.image = tk.PhotoImage(file=fn)
        img_ref= self.c.create_image(0,0,image=self.image,anchor="nw")
        self.refs.append(img_ref)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(SIZE)
    window = GUI(root)
    window.pack(expand=True, fill=tk.BOTH)
    root.mainloop()
