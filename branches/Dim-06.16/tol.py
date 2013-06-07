from math import *
from cad_canvas.default_tools import *
from cad_kernel import *

def l(startp = None):
    if canvas._more:
        if not startp:
            startp = canvas.point()
            l(startp)
        else:
            endp = canvas.point()
            canvas.line(startp, endp)
            l(endp)
    
def porras(cnt):
    p = canvas.point()
    p.new_formula(str(cnt))
    a = canvas.angleElement(p, "3.14/%s" % p.tag)
    for i in range(1, int(p.value()) - 1):
        a = canvas.angleElement(p, "3.14 / %s + %s" % (p.tag, a.tag))
    canvas.items.recalc()
    canvas.repaint()
        
def dist(startp, endp):
    x = abs(startp.x() - endp.x())
    y = abs(startp.y() - endp.y())
    return hypot(x,y)

def m():
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
    p.x.new_formula("%s" % str((p0.x + p1.x) / 2))
    p.y.new_formula("%s" % str((p0.y + p1.y) / 2))
    
    t = canvas.text(p, "round(hypot(abs(%s-%s),abs(%s-%s)),1)" % (p0.x.tag, p1.x.tag, p0.y.tag, p1.y.tag))

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

    p.fellows.update({p.x.tag:p.x,
                      p.y.tag:p.y,
                      p0.x.tag:p0.x,
                      p0.y.tag:p0.y,
                      p1.x.tag:p1.x,
                      p1.y.tag:p1.y,
                      })
    
    
    #canvas.items.recalc()
    canvas.repaint()


def mx():
    """x mitta"""
    p0 = canvas.point()
    p1 = canvas.point()
    
    l = canvas.line(p0, p1)
    l.arrows()

    p = canvas.point(canvas.xElement(100), canvas.yElement(100))
    p.x.new_formula("%s" % str((p0.x + p1.x) / 2))
    p.y.new_formula("%s" % str((p0.y + p1.y) / 2))
    
    t = canvas.text(p, "round(hypot(abs(%s-%s),abs(%s-%s)),1)" % (p0.x.tag, p1.x.tag, p0.y.tag, p1.y.tag))

    p0.hide()
    p1.hide()
    p0.x.hide()
    p0.y.hide()
    p1.x.hide()
    p1.y.hide()
    p.hide()
    p.x.hide()
    p.y.hide()
    
    canvas.items.recalc()
    canvas.repaint()
    
def my():
    """y mitta"""
    p0 = canvas.point()
    p1 = canvas.point()
    
    l = canvas.line(p0, p1)
    l.arrows()

    p = canvas.point(canvas.xElement(100), canvas.yElement(100))
    p.x.new_formula("%s" % str((p0.x + p1.x) / 2))
    p.y.new_formula("%s" % str((p0.y + p1.y) / 2))
    t = canvas.text(p, "round(hypot(abs(%s-%s),abs(%s-%s)),1)" % (p0.x.tag, p1.x.tag, p0.y.tag, p1.y.tag))

    p0.hide()
    p1.hide()
    p0.x.hide()
    p0.y.hide()
    p1.x.hide()
    p1.y.hide()
    p.hide()
    p.x.hide()
    p.y.hide()
    
    
    canvas.items.recalc()
    canvas.repaint()
    
def txt():
    p = canvas.point()
    canvas.text(canvas, p)    

def radp():
    p1 = canvas.point()
    p2 = canvas.point()
    a = canvas.angleElement(p1, "radp(%s,%s,%s,%s)" % (p1.x.tag, p1.y.tag, p2.x.tag, p2.y.tag))
    
    canvas.items.recalc()
    canvas.repaint()

def test(n):
    last = canvas.xElement("100")
    for i in range(n):
      last = canvas.xElement("%s + 1" % last.tag)