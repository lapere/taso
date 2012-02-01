from math import *

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
        
def dist(startp, endp):
    x = abs(startp.x() - endp.x())
    y = abs(startp.y() - endp.y())
    return hypot(x,y)

def mitta():
    l = canvas.line()
    l.arrows()
    l.value.new_formula(str(dist(l.startp, l.endp) * canvas._scale))
    l.entry(True)
        
