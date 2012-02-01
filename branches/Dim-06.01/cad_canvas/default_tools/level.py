from Tkinter import *
from item import Item       
from utils import *

class Level(Item):

    def __init__(self, canvas, value, typ):
        Item.__init__(self, canvas, typ, str(value))
        self.canvas = canvas
        self.active_fill = dict(fill="gray")
        self.passive_fill = dict(fill="")
        self.selected_fill = dict(fill="green")            

        self.line_kw_param = dict(width=1, fill="gray", tags=self.tag)
        self.create_visibles()
        
                
    def create_visibles(self):
        
        self.id = self.canvas.create_line(self.line_list_param,
                                          self.line_kw_param)
        self.canvas.tag_lower(self.tag)
        self.bindit()    
        return self.id
    
    def solve_line(self, other):
        
        nim = self.A() * other.B() - other.A() * self.B()
        
        if not nim:
            return 0, 0
            
        x_os = -self.C() *  other.B() - -other.C() *  self.B()
        y_os =  self.A() * -other.C() - other.A() * -self.C()

        x = float(x_os) / nim
        y = float(y_os) / nim

        return x, y
    
            

class _X(Level):

    def __init__(self, canvas, value):
        self.line_list_param = [value, 0, value, canvas["height"]]
        Level.__init__(self, canvas, value, "X")

    def repaint(self):
        self.canvas.coords(self.id, self(), 0, self(), self.canvas["height"])
            
    def A(self):
        return 1.0

    def B(self):
        return 0.0

    def C(self):
        x = self.canvas.coords(self.id)[0]
        return float(-self.A() * x - self.B())
        

class _Y(Level):

    def __init__(self, canvas, value):
        self.line_list_param = [0, value, canvas["width"], value]
        Level.__init__(self, canvas, value, "Y")

    def repaint(self):
        self.canvas.coords(self.id, 0, self(), self.canvas["width"], self())
        
    def A(self):
        return 0.0

    def B(self):
        return 1.0

    def C(self):
        y = self.canvas.coords(self.id)[1]
        return float(-self.A() - self.B() * y)

class _A(Level):

    def __init__(self, canvas, x, y, a):
        self.line_list_param = [0,100,200,300]
        Level.__init__(self, canvas, a, "A")
        
        self.x = x
        self.y = y
        self.a = a

        
    def repaint(self):

        _x = self.x()
        _y = self.y()
        a = self()
        
        if cos(a) and sin(a):
            l = [_x, _y, _x + cos(a) * 10, _y - sin(a) * 10]
        elif not sin(a):
            l = [_x, _y, _x, _y + 10]
        else:
            l = [_x, _y, _x + 10, _y]
        
        self.canvas.coords(self.id, l[0], l[1], l[2], l[3])
        
        if cos(a) > sin(a):
            x0,y0 = self.solve_line(self.canvas.y_e)
            x1,y1 = self.solve_line(self.canvas.y_0)
        else:
            x0,y0 = self.solve_line(self.canvas.x_e)
            x1,y1 = self.solve_line(self.canvas.x_0)
        
        self.canvas.coords(self.id, x0, y0, x1, y1)
        
        
    def A(self):
        y0 = self.canvas.coords(self.id)[1]
        y1 = self.canvas.coords(self.id)[3]
        return float(-(y0 - y1))

    def B(self):
        x0 = self.canvas.coords(self.id)[0]
        x1 = self.canvas.coords(self.id)[2]
        return float((x0 - x1))

    def C(self):
        x = self.canvas.coords(self.id)[0]
        y = self.canvas.coords(self.id)[1]
        return float(-self.A() * x - self.B() * y)

   
