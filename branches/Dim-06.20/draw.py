from Tkinter import *
from cmdmode import *
from default_tools.level import _X,_Y,_A
from default_tools.point import Point
from default_tools.line import Line
from default_tools.text import Txt
from math import *
x = None
y = None

current = PiPo.current
fun_syntax = dict()

def get_tags(_id):
        coord = current.canvas.coords(_id)
        tag_1 = "%04d,%04d" % (round(coord[0]) , round(coord[1]))
        tag_2 = "%04d,%04d" % (round(coord[2]) , round(coord[3]))
        return tag_1, tag_2

#-----------------------------------------------------------#
def xelement(*arg, **kw):
    "xelement(coord=(x,y))"
    x = kw.pop('coord')[0]

    current.item = _X(current.canvas, x)
    
fun_syntax["xelement"] = xelement.__doc__

#-----------------------------------------------------------#
def yelement(*arg, **kw):
    "yelement(coord=(x,y))"
    y = kw.pop('coord')[1]
    
    current.item = _Y(current.canvas, y)
    
fun_syntax["yelement"] = yelement.__doc__

#-----------------------------------------------------------#
def aelement(*arg, **kw):
    "aelement(point=(x,y), angle=(x,y))"
    x = kw["point"][0]
    y = kw["point"][1]

    if not current.canvas.items.has_key(x):
        x = _X(current.canvas, x)

    if not current.canvas.items.has_key(y):
        y = _Y(current.canvas, y)

    p = Point(current.canvas, x, y)

    if type(kw["angle"]) == tuple:
        a = hypot(abs(x-kw["angle"][0]),abs(y-kw["angle"][1]))
        
    current.item = _A(current.canvas, p, a)
    
fun_syntax["aelement"] = aelement.__doc__

#-----------------------------------------------------------#
def point(*arg, **kw):
    "point(coord=(x,y))"
    x, y = kw.pop('coord')

    current.item = current.canvas.point(x,y)
    
fun_syntax["point"] = point.__doc__

#-----------------------------------------------------------#
def arc(*arg, **kw):
    "arc(startp=(x,y), midp=(x,y), endp=(x,y))"
    
    arg = [current.canvas]
    try:
        if type(kw['direction']) == tuple:
            a = AngleBetweenTwoPoint(kw['startp'][0], kw['startp'][1], 
				kw['direction'][0], kw['direction'][1])
            kw['direction'] = -a
    except:
        pass
    current.item = _arc(*arg, **kw)
    bindit()
    
fun_syntax = dict(fun_syntax, arc=arc.__doc__)

#-----------------------------------------------------------#
def line(*arg, **kw):
    "line(startp=(x,y),endp=(x,y))"

    startp = kw.pop('startp')
    endp = kw.pop('endp')

    arg = [startp[0], startp[1], endp[0], endp[1]]
    kwr = dict(width=2)
    current.item = current.canvas.create_line(arg, kwr)
    bindit()

fun_syntax = dict(fun_syntax, line=line.__doc__)

#-----------------------------------------------------------#
def delete(*arg, **kw):
    "delete(tags=(None,))"
    
    current.canvas.delete(CURRENT)
fun_syntax = dict(fun_syntax, delete=delete.__doc__)

#-----------------------------------------------------------#

if __name__ == '__main__':
    print fun_syntax.keys()
