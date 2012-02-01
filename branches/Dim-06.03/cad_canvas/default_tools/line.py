from Tkinter import *
from item import *
from utils import *

class Line(Item):

    def __init__(self, canvas, startp, endp, style = dict(width=2)):
        Item.__init__(self, canvas, "L")

        self.org_x = int(startp.x)
        self.org_y = int(startp.y)

        self.startp = startp
        self.endp = endp
        
        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="black")
        self.selected_fill = dict(fill="green")

        self.style = style
        self.create_visibles()
        
    def create_visibles(self):
        
        self.style.update(dict(tags=self.tag))
    
        self.id = self.canvas.create_line(int(self.startp.x),
                                          int(self.startp.y),
                                          int(self.endp.x),
                                          int(self.endp.y),
                                          self.style)
        
        #Point must be above line for mouse_enter event
        self.canvas.tag_raise(self.startp.tag, self.tag)
        self.canvas.tag_raise(self.endp.tag, self.tag)
        
        #self.endp.hidden()
        #self.startp.hidden()

        self.bindit()
        #self.canvas.tag_bind(self.tag, "<B1-Motion>", self.move)
        
        self.canvas.repaint()
        return self.id
    
    def move(self, event):    
        pass
    
    def repaint(self):
        self.canvas.coords(self.tag, self.startp.get_x(),
                                     self.startp.get_y(),
                                     self.endp.get_x(),
                                     self.endp.get_y())  
    
    def get_ends(self):
        return self.startp, self.endp 
        
    def typ(self):
        if self.startp.x == self.endp.x:
            return "x"
        elif self.startp.y == self.endp.y:
            return "y"
        else:
            return "a"
        
