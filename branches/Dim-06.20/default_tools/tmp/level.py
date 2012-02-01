from Tkinter import *
from item import *   
from utils import *


class _X(VisualItem):

    def __init__(self, canvas, value, origo):
        VisualItem.__init__(self, canvas, value, origo)
        
        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="gray")
        self.selected_fill = dict(fill="green")
        self.hidden_fill = dict(fill="")            

        self.line_kw_param = dict(width=1, fill="gray", tags=self.tag)
        self.line_list_param = [self.value, 0, self.value, self.canvas["height"]]

        self.id = self.create_visibles()
        self.canvas.visuals[self.id] = self
        
    def create_visibles(self):        
        _id = self.canvas.create_line(self.line_list_param,
                                          self.line_kw_param)
        self.canvas.tag_lower(_id)
        self.bindit()
        self.canvas.tag_bind(_id, "<B1-Motion>", self.move)
        return _id

    def repaint(self):
        s = self.canvas._scale
        self.canvas.coords(self.id,
                           self.origo + self.value * s,
                           0,
                           self.origo + self.value * s,
                           self.canvas["height"])
                    
    def move(self, event):
        
        x = int(self.canvas.canvasx(event.x))
        s = self.canvas._scale
    
        if not self.value.names: 
           self.value.new_formula(str(x / s))
        
        self.canvas.repaint()
        
  

class _Y(VisualItem):

    def __init__(self, canvas, value, origo):
        VisualItem.__init__(self, canvas, value, origo)
        self.line_list_param = [0, self.value, canvas["width"], self.value]

        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="gray")
        self.selected_fill = dict(fill="green")
        self.hidden_fill = dict(fill="")            

        self.line_kw_param = dict(width=1, fill="gray", tags=self.tag)
        self.create_visibles()
        self.canvas.visuals[self.id] = self
                
    def create_visibles(self):
        self.id = self.canvas.create_line(self.line_list_param,
                                          self.line_kw_param)
        self.canvas.tag_lower(self.tag)
        self.bindit()
        self.canvas.tag_bind(self.tag, "<B1-Motion>", self.move)
        return self.id

    def repaint(self):
        s = self.canvas._scale
        self.canvas.coords(self.id,
                           0,
                           self.origo + self.value * s,
                           self.canvas["width"],
                           self.origo + self.value * s)
    def move(self, event):
        
        y = int(self.canvas.canvasx(event.y))
        s = self.canvas._scale
    
        if not self.value.names: 
           self.value.new_formula(str(y / s))
        
        self.canvas.repaint()
    
    

class _A(VisualItem):
    def __init__(self, canvas, point, a, origo):
        self.line_list_param = [0,100,200,300]
        VisualItem.__init__(self, canvas, a, origo)
    
        self.point = point
        self.point.fellows.update({self.tag:self})

        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="gray")
        self.selected_fill = dict(fill="green")
        self.hidden_fill = dict(fill="")            

        self.line_kw_param = dict(width=1, fill="gray", tags=self.tag)
        self.create_visibles()
        self.canvas.visuals[self.id] = self
                
    def create_visibles(self):
        
        self.id = self.canvas.create_line(self.line_list_param,
                                          self.line_kw_param)
        self.canvas.tag_lower(self.tag)
        if not self.visible:
            self.hide()
        self.bindit()
        self.canvas.tag_bind(self.tag, "<B1-Motion>", self.move)
        return self.id

    def move(self, event):

        x = int(self.canvas.canvasx(event.x))
        y = int(self.canvas.canvasy(event.y))

        xx = float(self.point.x)
        yy = float(self.point.y)

        a =  RadBetweenTwoPoint(x,y,xx,yy)
        
        if not self.value.names: 
           self.value.new_formula(str(a))
        
        self.canvas.repaint()
        
    def repaint(self):
        x = self.point.x
        y = self.point.y
        _x = self.origo + float(x) * self.canvas._scale
        _y = self.origo + float(y) * self.canvas._scale
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
        
    def A(self):
        y0 = float(self.point.y)     #self.canvas.coords(self.id)[1]
        y1 = y0 - sin(float(self))  #self.canvas.coords(self.id)[3]
        return float(-(y0 - y1))

    def B(self):
        x0 = float(self.point.x)	#self.canvas.coords(self.id)[0]
        x1 = cos(float(self)) + x0	#self.canvas.coords(self.id)[2]
        return float((x0 - x1))

    def C(self):
        x = float(self.point.x)	#self.canvas.coords(self.id)[0]
        y = float(self.point.y)	#self.canvas.coords(self.id)[1]
        return float(-self.A() * x - self.B() * y)
