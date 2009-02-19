#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
import pickle


class Letter(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.canvas = Canvas(self, height=600, width=600, bg="white")
        self.canvas.pack(expand=True, fill=BOTH)

        self.letters = pickle.load(open('save.p'))
        for c,l in enumerate(self.letters):
            self.do(l,c)

    def do(self, letter, count):
        for line in self.letters[letter]:
            tag = self.canvas.create_line(line, capstyle="round",
                                          tags=str(count))
            self.canvas.scale(tag, 0, 0, 4, 4)
            self.canvas.move(tag, (count*50) % 600, ((count*50)/600)*60)
                
        
   
if __name__ == '__main__':
    root = Tk()
    g = Letter(root)
    g.pack()
    root.mainloop()

