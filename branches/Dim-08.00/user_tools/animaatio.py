from math import *
from default_tools import *
import  current
canvas = current.canvas

def ukko():

    p = canvas.point()
    
    p1 = canvas.point(p.x, p.y-40)
    p2 = canvas.point(p.x-10, p.y-20)
    p3 = canvas.point(p.x, p.y-20)
    p4 = canvas.point(p.x+20, p.y-20)
    p5 = p
    p6 = canvas.point(p.x, p.y+20)
    p7 = canvas.point(p.x-10, p.y+30)
    p8 = canvas.point(p.x+10, p.y+30)

    l1 = canvas.line(p1,p3)
    l2 = canvas.line(p2,p3)
    l3 = canvas.line(p4,p3)
    l4 = canvas.line(p5,p3)
    l5 = canvas.line(p5,p6)
    l6 = canvas.line(p6,p7)
    l7 = canvas.line(p6,p8)

    st = dict(capstyle="round", width=10)

    #for i in l1, l2, l3, l4, l5, l6, l7:
    #    i.style.update(st)
        
    canvas.items.recalc()
    canvas.repaint()
