#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
import pickle


class Letter(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
	self.cursor = 10
        self.canvas = Canvas(self, height=600, width=600, bg="white")
        self.canvas.pack(expand=True, fill=BOTH)

        self.letters = pickle.load(open('save.p'))
        for c,l in enumerate(self.letters):
            self.do(l,c)

    def do(self, letter, count):
	w = [0]
	t = str(count)
        for line in self.letters[letter]:
            tag = self.canvas.create_line(line, capstyle="round",
                                          tags=t)
	    w = [max(line+w)]
            #self.canvas.scale(tag, 0, 0, 1, 1)
	    self.canvas.move(tag, self.cursor, 0)

        self.cursor = self.cursor + w[0]
                

root = Tk()
g = Letter(root)
g.pack()

g.canvas.focus_set()
g.canvas.update_idletasks()
g.canvas.postscript(colormode="gray", file="fn.ps")

root.mainloop()

