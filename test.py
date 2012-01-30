#!/usr/bin/python
# -*- coding: utf-8 -*-
#P.R

from Tkinter import *
from cad_canvas import *
from cad_canvas.MenuFrame import MenuFrame
from command_line import *
from cad_kernel import *

import imp
import types
import current

class Test:
    
    canvas = None

    def __init__(self, root):
        
        
        #canvas = cad_canvas(root, width = 600, height= 400, bg="white")
        txt = command_line.CmdText(root)
        self.mf = MenuFrame(root)
        self.mf.pack(fill=X)
        txt.canvas.pack(expand=1, fill=BOTH)
        txt.pack(fill=X)
        current.canvas = txt.canvas
        
        self.mf.addCommand("Tiedosto","Uusi", txt.canvas._new)
        self.mf.addCommand("Tiedosto","Avaa", txt.canvas._open)
        self.mf.addCommand("Tiedosto","Avaa DB", txt.canvas.open_db)
        self.mf.addCommand("Tiedosto","Tallenna", txt.canvas._save)
        self.mf.addCommand("Tiedosto","Tulosta", txt.canvas._print)
        self.mf.addCommand("Tiedosto","Status", txt.canvas.print_status)
        self.mf.addCommand("Tiedosto","Poistu", root.quit)

        self.mf.addCommand("Muokkaa","Poista", txt.canvas._delete)
        self.mf.addCommand("Muokkaa","Valitse", txt.canvas._select)
        self.mf.addCommand("Muokkaa","Valitse_alue", txt.canvas.select_rect)
        self.mf.addCommand("Muokkaa","Piilota", txt.canvas.hide)
        self.mf.addCommand("Muokkaa","Älä piilota", txt.canvas.unhide)

        self.mf.addCommand("Piirrä","Piste", txt.canvas.point)
        self.mf.addCommand("Piirrä","Viiva", txt.canvas.line)
        self.mf.addCommand("Piirrä","Teksti", txt.canvas.text)

        self.mf.addCommand("Elementti","X", txt.canvas.xElement)
        self.mf.addCommand("Elementti","Y", txt.canvas.yElement)
        self.mf.addCommand("Elementti","Kulma", txt.canvas.angleElement)
        self.mf.addCommand("Elementti","Ympyrä", txt.canvas.circleElement)
        
    def load_user_tools(self):
        "lataa user tools"
        fp, pathname, description = imp.find_module("user_tools")

        try:
            module = imp.load_module("user_tools", fp, pathname, description)
            self.__dict__.update(module.__dict__)
            for tool in module.__dict__:
                if tool[:2] != "__":
                     for i in dir(module.__dict__[tool]):
                        if i[:2] != "__":
                           fun = module.__dict__[tool].__dict__[i]
                           if type(fun) == types.FunctionType:
                               self.mf.addCommand(tool, i, fun)

        finally:
            if fp:
                fp.close()

if __name__ == '__main__':
    root = Tk()
    w, h = root.maxsize()
    root.geometry("%dx%d" % (w, h))
    t = Test(root)
    from user_tools import *
    t.load_user_tools()
    root.mainloop()
    root.destroy()

    
