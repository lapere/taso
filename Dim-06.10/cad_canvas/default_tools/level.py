from Tkinter import *
from item import VisualYItem, VisualXItem, VisualAngleItem     
from utils import *


class _X(VisualXItem):

    def __init__(self, canvas, value):
        VisualXItem.__init__(self, canvas, "X", value)
        self.line_list_param = [value, 0, value, canvas["height"]]

        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="gray")
        self.selected_fill = dict(fill="green")
        self.hidden_fill = dict(fill="")            

        self.line_kw_param = dict(width=1, fill="gray", tags=self.tag)
        self.create_visibles()
        
                
    def create_visibles(self):
        
        self.id = self.canvas.create_line(self.line_list_param,
                                          self.line_kw_param)
        self.canvas.tag_lower(self.tag)
        self.bindit()
        self.repaint()
        return self.id

    def repaint(self):
        s = self.canvas._scale
        self.canvas.coords(self.id,
                           float(self.value * s),
                           0,
                           float(self.value * s),
                           self.canvas["height"])

    def get_x(self):
        return self() * self.canvas._scale

class _Y(VisualYItem):

    def __init__(self, canvas, value):
        VisualYItem.__init__(self, canvas, "Y", value)
        self.line_list_param = [0, value, canvas["width"], value]

        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="gray")
        self.selected_fill = dict(fill="green")
        self.hidden_fill = dict(fill="")            

        self.line_kw_param = dict(width=1, fill="gray", tags=self.tag)
        self.create_visibles()
        
                
    def create_visibles(self):
        self.id = self.canvas.create_line(self.line_list_param,
                                          self.line_kw_param)
        self.canvas.tag_lower(self.tag)
        self.bindit()
        self.repaint()
        return self.id

    def repaint(self):
        s = self.canvas._scale
        self.canvas.coords(self.id,
                           0,
                           float(self.value * s),
                           self.canvas["width"],
                           float(self.value * s))

    def get_y(self):
        return self() * self.canvas._scale

class _A(VisualAngleItem):

    def __init__(self, canvas, x, y, a):
        self.line_list_param = [0,100,200,300]
        VisualAngleItem.__init__(self, canvas, "A", x, y, a)
    
    
        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="gray")
        self.selected_fill = dict(fill="green")
        self.hidden_fill = dict(fill="")            

        self.line_kw_param = dict(width=1, fill="gray", tags=self.tag)
        self.create_visibles()
        
                
    def create_visibles(self):
        
        self.id = self.canvas.create_line(self.line_list_param,
                                          self.line_kw_param)
        self.canvas.tag_lower(self.tag)
        self.bindit()    
        return self.id
    
    def repaint(self):

        _x = float(self.value.x) * self.canvas._scale
        _y = float(self.value.y) * self.canvas._scale
        a = float(self.value)   

        if cos(a) and sin(a):
            l = [_x - cos(a) * 10,
                 _y + sin(a) * 10,
                 _x + cos(a) * 10,
                 _y - sin(a) * 10]
        elif not sin(a):
            l = [_x, _y - 10, _x, _y + 10]
        else:
            l = [_x - 10, _y, _x + 10, _y]
        m = float(max(self.canvas["width"], self.canvas["height"]))
        self.canvas.coords(self.id, l[0], l[1], l[2], l[3])        
        self.canvas.scale(self.id, _x, _y, m/10, m/10)
        

