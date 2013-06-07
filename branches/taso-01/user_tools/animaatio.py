import Image
from math import *
from default_tools import *
import  current
canvas = current.canvas
cnt = 0

def ukko():

    p = canvas.point()
    
    p1 = canvas.point(p.x, p.y-40)
    p2 = canvas.point(p.x-20, p.y-20)
    p3 = canvas.point(p.x, p.y-20)
    p4 = canvas.point(p.x+20, p.y-20)
    k1 = canvas.point(p.x-30, p.y-10)
    k2 = canvas.point(p.x+30, p.y-10)
    p5 = p
    p6 = canvas.point(p.x, p.y+20)
    p7 = canvas.point(p.x-10, p.y+30)
    p8 = canvas.point(p.x+10, p.y+30)
    p9 = canvas.point(p.x-10, p.y+60)
    p10 = canvas.point(p.x+10, p.y+60)

    l1 = canvas.line(p1,p3)
    l2 = canvas.line(p2,p3)
    l3 = canvas.line(p4,p3)
    l4 = canvas.line(p5,p3)
    l5 = canvas.line(p5,p6)
    l6 = canvas.line(p6,p7)
    l7 = canvas.line(p6,p8)
    l8 = canvas.line(p7,p9)
    l9 = canvas.line(p8,p10)
    l10 = canvas.line(p2,k1)
    l11 = canvas.line(p4,k2)

    
    canvas.repaint()

def save():
    global cnt
    canvas.postscript(colormode="gray", file="tmp.ps")
    img = Image.open("tmp.ps")
    img.save("kuvat/frame_%04d.jpg" % cnt, "JPEG")
    cnt += 1   
    
