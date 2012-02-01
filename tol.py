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

class m(item.VisualItem):
    def __init__(self):
        item.VisualItem.__init__(self, canvas, "M")
        """x mitta"""
        print "valitse elementti"
        a0 = canvas.angleElement()
        print "tee elementti"
        a1 = canvas.angleElement(value = "%s" % a0.tag)
        print "mittaviivan alkupiste"
        p0 = canvas.point()
        a3 = canvas.angleElement(point=p0, value = "pi/2+%s" % a0.tag)
        print "mittaviivan loppupiste"
        p1 = canvas.point()
        
        l = canvas.line(p0, p1)
        l.arrows()

        p = canvas.point(canvas.xElement(100), canvas.yElement(100))
        p.x.value.new_formula("(%s + %s) / 2.0" % (p0.x.tag, p1.x.tag))
        p.y.value.new_formula("(%s + %s) / 2.0" % (p0.y.tag, p1.y.tag))
        
        t = canvas.text(p, "round(hypot(abs(%s-%s),abs(%s-%s)))" % (p0.x.tag, p1.x.tag, p0.y.tag, p1.y.tag))

        a3.hide()
        p0.hide()
        p1.hide()
        p0.x.hide()
        p0.y.hide()
        p1.x.hide()
        p1.y.hide()
        p.hide()
        p.x.hide()
        p.y.hide()

        p.fellows.update({self.tag:self,
                          p.x.tag:p.x,
                          p.y.tag:p.y,
                          p0.x.tag:p0.x,
                          p0.y.tag:p0.y,
                          p1.x.tag:p1.x,
                          p1.y.tag:p1.y,
                          })
        
        
        canvas.items.recalc()
        canvas.repaint()


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
        
