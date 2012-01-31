#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
from cad_canvas import *
from cad_canvas.MenuFrame import *
from command_line.command_line import *
from cad_kernel import *

root = Tk()
w, h = root.maxsize()
root.geometry("%dx%d" % (w/2, h/2))

ic = InteractiveConsole()

menu_frame = MenuFrame(root)
canvas = cad_canvas(root, ic, width = 600, height= 400, bg="white")


ic.locals["canvas"] = canvas
ic.runsource("from default_tools import *")
ic.runsource("draw.canvas = canvas")

command_line = CommandLine(root, canvas, ic)

menu_frame.pack(fill=X)
canvas.pack(expand=1, fill=BOTH)
command_line.pack(fill=X)

root.mainloop()
root.destroy()

