from Tkinter import *
from item import *
from utils import *
from cad_kernel.db import Item

class Line(VisualItem):

    def __init__(self, canvas, startp, endp):
        VisualItem.__init__(self, canvas, "L", None)#"%s,%s" % (startp.tag, endp.tag))

        self.startp = startp
        self.endp = endp
        startp.fellows.update({self.tag:self})
        endp.fellows.update({self.tag:self})
        
        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="black")
        self.selected_fill = dict(fill="green")
        self.hidden_fill = dict(fill="")
        self.style = dict()
        self.create_visibles()
        
    def create_visibles(self):
        
        self.style.update(dict(tags=self.tag))
        
        self.id = self.canvas.create_line(0,0,0,0,self.style)
        
        #Point must be above line for mouse_enter event
        self.canvas.tag_raise(self.startp.tag, self.tag)
        self.canvas.tag_raise(self.endp.tag, self.tag)
        
        if not self.visible:
            self.hide()
        self.bindit()
        
        return self.id
    
    def move(self, event):    
        pass
    
    def repaint(self):

        
        x0 = self.startp.x
        y0 = self.startp.y
        x1 = self.endp.x
        y1 = self.endp.y
        s = self.canvas._scale
        self.canvas.coords(self.id, x0*s, y0*s, x1*s, y1*s)                              
        self.canvas.itemconfig(self.id, self.style)
    
    def get_ends(self):
        return self.startp, self.endp 
        
    def typ(self):
        if self.startp.y == self.endp.y:
            return "y"
        elif self.startp.x == self.endp.x:
            return "x"
        else:
            return "a"

    def arrows(self):
        self.style.update(dict(width=1, arrow=BOTH, arrowshape=(16,16,2)))
        self.canvas.itemconfig(self.id, width=1, arrow=BOTH, arrowshape=(16,16,2))

    def pen(self, value):
        self.style.update(dict(width=value))
        self.canvas.itemconfig(self.id, width=value)
