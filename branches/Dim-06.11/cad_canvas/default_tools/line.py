from Tkinter import *
from item import *
from utils import *

class Line(VisualItem):

    def __init__(self, canvas, startp, endp):
        VisualItem.__init__(self, canvas, "L")

        #self.org_x = startp.x()
        #self.org_y = endp.y()

        self.startp = startp
        self.endp = endp
        
        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="black")
        self.selected_fill = dict(fill="green")
        self.hidden_fill = dict(fill="")
        self.style = dict()
        self.create_visibles()
        
    def create_visibles(self):
        
        self.style.update(dict(tags=self.tag))
        
        self.id = self.canvas.create_line(self.startp.x(),
                                          self.startp.y(),
                                          self.endp.x(),
                                          self.endp.y(),
                                          self.style)
        
        #Point must be above line for mouse_enter event
        self.canvas.tag_raise(self.startp.tag, self.tag)
        self.canvas.tag_raise(self.endp.tag, self.tag)
        
        #self.endp.hidden()
        #self.startp.hidden()

        self.bindit()
        #self.canvas.tag_bind(self.tag, "<B1-Motion>", self.move)
        
        #self.repaint()
        return self.id
    
    def move(self, event):    
        pass
    
    def repaint(self):
        self.canvas.coords(self.id, self.startp.x.get_x(),
                                     self.startp.y.get_y(),
                                     self.endp.x.get_x(),
                                     self.endp.y.get_y())
    
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
