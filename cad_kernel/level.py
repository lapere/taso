from Tkinter import *
from fellow import *
from item import Item       
from spreadsheet import Formula
from utils import *

class Level(Item):

    def __init__(self, canvas, value, typ):
        Item.__init__(self, canvas, typ)
        
        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="grey")
        self.selected_fill = dict(fill="green")            

        self.line_kw_param = dict(width=1, fill="gray", tags=self.tag)
        self.create_visibles()
        
                
    def create_visibles(self):
        
        self.id = self.canvas.create_line(self.line_list_param,
                                          self.line_kw_param)
        self.canvas.tag_lower(self.tag)
        self.bindit()    
        return self.id
  
    def repaint(self):
        self(self.canvas.S[self.tag].value)
    
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
        self.canvas.S[self.tag] = Formula(str(value))

    def __call__(self, x=None):
        if x:
            self.canvas.coords(self.id, x, 0, x, self.canvas["height"])
        else:
            return float(self.canvas.coords(self.id)[0])
            
    def A(self):
        return 1.0

    def B(self):
        return 0.0

    def C(self):
        #x = self.canvas.coords(self.id)[0]
        return float(-self.A() * self() - self.B())
        

class _Y(Level):

    def __init__(self, canvas, value):
        self.line_list_param = [0, value, canvas["width"], value]
        Level.__init__(self, canvas, value, "Y")
        self.canvas.S[self.tag] = Formula(str(value))

    def __call__(self, y=None):
        if y:
            self.canvas.coords(self.id, 0, y, self.canvas["width"], y)
        else:
            return float(self.canvas.coords(self.id)[1])
    
    def A(self):
        return 0.0

    def B(self):
        return 1.0

    def C(self):
        #y = self.canvas.coords(self.id)[1]
        return float(-self.A() - self.B() * self())

class _A(Level):

    def __init__(self, canvas, x, y, a):
        self.line_list_param = [0,100,200,300]
        Level.__init__(self, canvas, None, "A")
        
        self.x = x
        self.y = y
        self.a = a

        self.canvas.S[self.tag] = Formula(str(a))
        self.repaint()
        
    def __call__(self, a=None):
        if a != None:
            _x,_y = self.x.solve_line(self.y)
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
            
        else:
            return self.a
    
    def A(self):
        y0 = self.y()   #self.canvas.coords(self.id)[1]
        y1 = #self.canvas.coords(self.id)[3]
        return float(-(y0 - y1))

    def B(self):
        x0 = #self.canvas.coords(self.id)[0]
        x1 = #self.canvas.coords(self.id)[2]
        return float((x0 - x1))

    def C(self):
        x = #self.canvas.coords(self.id)[0]
        y = #self.canvas.coords(self.id)[1]
        return float(-self.A() * x - self.B() * y)

   
