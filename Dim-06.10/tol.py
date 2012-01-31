from math import *
from cad_canvas.default_tools import *

def l(startp = None):
    if canvas._more:
        if not startp:
            startp = canvas.point()
            l(startp)
        else:
            endp = canvas.point()
            canvas.line(startp, endp)
            l(endp)

def porras():
    p = canvas.point()
    for i in range(16):
        canvas.angleElement(p, (pi/16)*i)
    canvas.items.recalc()
    canvas.repaint()
        
def dist(startp, endp):
    x = abs(startp.x() - endp.x())
    y = abs(startp.y() - endp.y())
    return hypot(x,y)

def m():
    """mitta"""
    l = canvas.line()
    l.arrows()

    p = canvas.point(canvas.xElement(100), canvas.yElement(100))
    p.x.value.new_formula("(%s + %s) / 2.0" % (l.startp.x.tag, l.endp.x.tag))
    p.y.value.new_formula("(%s + %s) / 2.0" % (l.startp.y.tag, l.endp.y.tag))
    p.hide()
    p.x.hide()
    p.y.hide()
    t = canvas.text(p, dist(l.startp, l.endp))
    canvas.items.recalc()
    canvas.repaint()
    
    
def txt():
    p = canvas.point()
    canvas.text(canvas, p)    
        
