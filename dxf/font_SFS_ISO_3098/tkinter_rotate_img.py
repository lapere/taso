from Tkinter import *
import math
from itertools import *
from test import Letter
root = Tk()
l = Letter(root)
l.pack()
c = l.canvas

center = 300, 300

def getangle(event):
    dx = c.canvasx(event.x) - center[0]
    dy = c.canvasy(event.y) - center[1]
    try:
        return complex(dx, dy) / abs(complex(dx, dy))
    except ZeroDivisionError:
        return 0.0 # cannot determine angle

def press(event):
    # calculate angle at start point
    global start
    start = getangle(event)

def motion(event):
    # calculate current angle relative to initial angle
    global start
    angle = getangle(event) / start
    offset = complex(center[0], center[1])
    newxy = []
    for tag in range(len(l.letters)):
        lst =  c.coords(str(tag))
        iter = list(izip(*[chain(lst, repeat(0, 2-1))]*2))
        for x, y in iter:
            v = angle * (complex(x, y) - offset) + offset
            newxy.append(v.real)
            newxy.append(v.imag)
        c.coords(str(tag), *newxy)

c.bind("<Button-1>", press)
c.bind("<B1-Motion>", motion)

root.mainloop()
