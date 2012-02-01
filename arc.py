from Tkinter import *
from fellow import *
from item import *
from create_arc import _arc
from math import cos, sin

class Arc(Item):

    def __init__(self, canvas, **kw):
        Item.__init__(self, canvas, "C")

        self.points = kw
        self.endp = kw["endp"]
        self.active_fill = dict(outline="red")
        self.passive_fill = dict(outline="black")
        self.selected_fill = dict(outline="green")

        for p in self.points:
            if self.points[p]:
                self.new_fellow(self.points[p])
                self.points[p].new_fellow(self)
        
        self.create_visibles()
        

    def parse_args(self):
        self.args = dict()
        
        for p in self.points:
            point = self.points[p]
            if point:
                self.args[p] = (point.x(), point.y())
            else:
                self.args[p] = None
                
    def create_visibles(self):

        self.parse_args()
        self.id = _arc(self.canvas, **self.args)
        self.canvas.addtag_withtag(self.tag, self.id) 

        self.set_endpoint()
        
        #Point must be above line for mouse_enter event
        
        for p in self.points:
            if self.points[p]:
                self.canvas.tag_raise(self.points[p].tag, self.tag)
                #self.points[p].hidden()

        self.bindit()

        return self.id
    
    def repaint(self):
        self.canvas.delete(self.id)
        self.create_visibles()
    
    def set_endpoint(self):
        angle = self.canvas.itemcget(self.id,  "extent")
        astart = self.canvas.itemcget(self.id,  "start")
        coords = self.canvas.coords(self.id)

        r = abs(coords[0] - coords[2]) / 2
        angle = float(astart) - float(angle)

        print angle
        x = cos(angle) * r + coords[0] + r
        y = sin(angle) * r + coords[1] + r

        self.endp.x(x)
        self.endp.y(y)
        
        
        

        
