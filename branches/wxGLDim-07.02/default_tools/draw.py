import current
import cad_canvas


def __get_point(event=None):
    return  current.canvas.getPoint()

def point(event=None):
    p = __get_point()
    cad_canvas.vp.Point(current.canvas, current.db, "P", p)

def points(event=None):
    current.canvas.reset_buffer()
    p = __get_point()
    while p:
        cad_canvas.vp.Point(current.canvas, current.db, "P", p)
        p = __get_point()

def lines(event=None):
    sp = __get_point()
    ep = __get_point()
    while ep:
        l = cad_canvas.vp.Line(current.canvas, current.db, "L", sp+ep)
        l.repaint()
        current.canvas.SwapBuffers()
        sp = ep
        ep = __get_point()
    
        
            


