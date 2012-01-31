#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
from scroll import *
from MenuFrame import MenuFrame

class Test:
    
    canvas = None

    def __init__(self):
        root = Tk()
        w, h = root.maxsize()
        root.geometry("%dx%d" % (w, h))
        
        canvas_frame = ScrolledCanvas(root)
        menu_frame = MenuFrame(root)

        menu_frame.pack(fill=X)
        canvas_frame.pack(expand=1, fill=BOTH)
        
        
        canvas = canvas_frame.canv

        menu_frame.addCommand("Tiedosto","Avaa", canvas._open)
        menu_frame.addCommand("Tiedosto","Tallenna", canvas._save)
        menu_frame.addCommand("Tiedosto","Tulosta", canvas._print)
        menu_frame.addCommand("Tiedosto","Status", canvas.print_status)
        menu_frame.addCommand("Tiedosto","Poistu", root.quit)

        menu_frame.addCommand("Muokkaa","Poista", canvas._delete)

        menu_frame.addCommand("Piirrä","Piste", canvas.e_p)
        menu_frame.addCommand("Piirrä","Viiva", canvas.line)
        menu_frame.addCommand("Piirrä","Mitta", canvas.dimension)

        menu_frame.addCommand("Elementti","X", canvas.e_x)
        menu_frame.addCommand("Elementti","Y", canvas.e_y)
        menu_frame.addCommand("Elementti","Kulma", canvas.e_a)

        menu_frame.addCommand("Kaari",'3 Points', canvas.arc_3p)
        menu_frame.addCommand("Kaari",'Start,Center,End', canvas.arc_sce)
       

        root.mainloop()
        root.destroy()
        
if __name__ == '__main__':
    t = Test()
