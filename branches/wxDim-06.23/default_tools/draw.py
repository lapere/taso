from math import *
from tools import *

#-----------------------------------------------------------#
def xelement(*arg, **kw):
    "xelement(coord=(x,y))"
    x = kw.pop('coord')[0]
    canvas.current_item = item.Xelement(canvas, x)
    

#-----------------------------------------------------------#
def yelement(*arg, **kw):
    "yelement(coord=(x,y))"
    y = kw.pop('coord')[1]

    canvas.current_item = vp.HorizontalLine(canvas, y, 0).id
    

#-----------------------------------------------------------#
def aelement(*arg, **kw):
    "aelement(point=(x,y), angle=(x,y))"
    x = kw["point"][0]
    y = kw["point"][1]

    if type(kw["angle"]) == tuple:
        a = radp(x, y, kw["angle"][0], kw["angle"][1])
        
    canvas.current_item = vp.AngledLine(canvas, x, y, a, 0).id
    

#-----------------------------------------------------------#
def point(*arg, **kw):
    "point(endp=(x,y))"
    x, y = kw.pop('endp')
    canvas.current_item = vp.Point(canvas, x, y, 0).id
    

#-----------------------------------------------------------#
def arc(*arg, **kw):
    "arc(startp=(x,y), midp=(x,y), endp=(x,y))"
    
    arg = [canvas]
    try:
        if type(kw['direction']) == tuple:
            a = AngleBetweenTwoPoint(kw['startp'][0], kw['startp'][1], 
				kw['direction'][0], kw['direction'][1])
            kw['direction'] = -a
    except:
        pass
    canvas.current_item = _arc(*arg, **kw)
    bindit()
    
#-----------------------------------------------------------#
def line(*arg, **kw):
    "line(startp=(x,y),endp=(x,y))"

    startp = kw.pop('startp')
    endp = kw.pop('endp')
    canvas.current_item = vp.Line(canvas, startp[0], startp[1], endp[0], endp[1], 0).id
    
#-----------------------------------------------------------#
def delete(*arg, **kw):
    "delete(tags=(None,))"
    
    canvas.current_item.delete(CURRENT)

