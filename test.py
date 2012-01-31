#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
from scroll import *



class Test:
    
    canvas = None

    def __init__(self):
        root = Tk()
        
        frame = ScrolledCanvas(root)
        button_frame = Frame(root)
        
        
        frame.pack(expand=1, fill=BOTH)
        button_frame.pack(fill=X)
        
        canvas = frame.canv
        
        button_line = Button(button_frame, text="viiva", command=canvas.line)
        button_point = Button(button_frame, text="piste", command=canvas.getPoint)
        button_elex = Button(button_frame, text="pysty-elementti", command=canvas.xelement)
        button_eley = Button(button_frame, text="vaaka-elementti", command=canvas.yelement)
        button_dimx = Button(button_frame, text="x-mitta", command=canvas.xdimension)
        button_dimy = Button(button_frame, text="y-mitta", command=canvas.ydimension)
        button_status = Button(button_frame, text="status", command=canvas.print_status)
        button_delete = Button(button_frame, text="delete", command=canvas._delete)
        button_print = Button(button_frame, text="print", command=canvas._print)
        button_open = Button(button_frame, text="open", command=canvas._open)
        button_save = Button(button_frame, text="save", command=canvas._save)

        button_line.pack(side=LEFT)
        button_point.pack(side=LEFT)
        button_elex.pack(side=LEFT)
        button_eley.pack(side=LEFT)
        button_dimx.pack(side=LEFT)
        button_dimy.pack(side=LEFT)
        button_delete.pack(side=LEFT)
        button_print.pack(side=LEFT)
        button_open.pack(side=LEFT)
        button_save.pack(side=LEFT)
        button_status.pack(side=LEFT)

        root.mainloop()

if __name__ == '__main__':
    t = Test()
