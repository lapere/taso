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
    p.value.new_formula("16")
    a = canvas.angleElement(p, "3.14/%s" % p.tag)
    for i in range(1, int(p.value()) - 1):
        a = canvas.angleElement(p, "3.14 / %s + %s" % (p.tag, a.tag))
    canvas.items.recalc()
    canvas.repaint()
        
def dist(startp, endp):
    x = abs(startp.x() - endp.x())
    y = abs(startp.y() - endp.y())
    return hypot(x,y)

def mx():
    """x mitta"""
    l = canvas.line()
    l.arrows()
    l.startp.hide()
    l.endp.hide()

    p = canvas.point(canvas.xElement(100), canvas.yElement(100))
    p.x.value.new_formula("(%s + %s) / 2.0" % (l.startp.x.tag, l.endp.x.tag))
    p.y.value.new_formula(l.startp.y.tag)
    p.hide()
    p.x.hide()
    p.y.hide()
    t = canvas.text(p, "round(abs(%s - %s), 1)" % (l.startp.x.tag, l.endp.x.tag))
    canvas.items.recalc()
    canvas.repaint()

def my():
    """y mitta"""
    l = canvas.line()
    l.arrows()
    l.startp.hide()
    l.endp.hide()
    x = canvas.xElement(100)
    y = canvas.yElement(100)  
    p = canvas.point(x, y)
    p.y.value.new_formula("(%s + %s) / 2.0" % (l.startp.y.tag, l.endp.y.tag))
    p.x.value.new_formula(l.startp.x.tag + " - 20")
    p.hide()
    p.x.hide()
    p.y.hide()
    t = canvas.text(p, "round(abs(%s - %s), 1)" % (l.startp.y.tag, l.endp.y.tag))
    
    canvas.items.recalc()
    canvas.repaint()
    
    
def txt():
    p = canvas.point()
    canvas.text(canvas, p)    
        
