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
        
