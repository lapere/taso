import current
import cad_canvas
import wx
import sys
def get_point():
    return  current.canvas.getPoint()

def point():
    p = get_point()
    cad_canvas.vp.Point(current.canvas, current.db, "P", p)

def points():    
    p = get_point()
    while p:
        cad_canvas.vp.Point(current.canvas, current.db, "P", p)
        p = get_point()

def lines():
    sp = get_point()
    ep = get_point()
    while ep:
        l = cad_canvas.vp.Line(current.canvas, current.db, "L", sp+ep)
        l.repaint()
        sp = ep
        ep = get_point()
        current.canvas.SwapBuffers()
            


