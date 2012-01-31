#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
from cad_canvas import *
from cad_canvas.MenuFrame import MenuFrame
from cmd import *

class Test:
    
    canvas = None

    def __init__(self):
        root = Tk()
        w, h = root.maxsize()
        root.geometry("%dx%d" % (w, h))
        
        #canvas = cad_canvas(root, width = 600, height= 400, bg="white")
        txt = CmdText(root)
        menu_frame = MenuFrame(root)
        menu_frame.pack(fill=X)
        txt.canvas.pack(expand=1, fill=BOTH)
        txt.pack(fill=X)

        menu_frame.addCommand("Tiedosto","Avaa", txt.canvas._open)
        menu_frame.addCommand("Tiedosto","Tallenna", txt.canvas._save)
        menu_frame.addCommand("Tiedosto","Tulosta", txt.canvas._print)
        menu_frame.addCommand("Tiedosto","Status", txt.canvas.print_status)
        menu_frame.addCommand("Tiedosto","Poistu", root.quit)

        menu_frame.addCommand("Muokkaa","Poista", txt.canvas._delete)

        menu_frame.addCommand("Piirrä","Piste", txt.canvas.point)
        menu_frame.addCommand("Piirrä","Viiva", txt.canvas.line)

        menu_frame.addCommand("Elementti","X", txt.canvas.xElement)
        menu_frame.addCommand("Elementti","Y", txt.canvas.yElement)
        menu_frame.addCommand("Elementti","Kulma", txt.canvas.angleElement)

        root.mainloop()
        root.destroy()
        
if __name__ == '__main__':
    t = Test()
