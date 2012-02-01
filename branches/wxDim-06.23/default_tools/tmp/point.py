from Tkinter import *
from line import *
from item import *
import level

class _Point(VisualItem):

    def __init__(self, canvas, value, x, y):
        VisualItem.__init__(self, canvas, value, origo=(0,0))
        self.x = x
        self.y = y
        self.active_fill = dict(fill="red", outline="black")
        self.passive_fill = dict(fill="", outline="gray")
        self.selected_fill = dict(fill="green", outline="black")
        self.hidden_fill = dict(fill="", outline="")            

        self.create_visibles()
        self.canvas.visuals[self.id] = self
        
    def create_visibles(self):
        
        self.id = self.canvas.create_rectangle(0, 0, 0, 0,
                                               fill="",
                                               outline="black",
                                               tags=self.tag)
        
        
            
        self.bindit()
        
        #self.canvas.tag_bind(self.tag, "<ButtonRelease-1>", self.join)
        self.repaint()
        return self.id

    def repaint(self):
        #x = self.origo[0] + self.x() * self.canvas._scale
        #y = self.origo[1] + self.y() * self.canvas._scale
        x = self.canvas.coords(self.x.id)[0]
        y = self.canvas.coords(self.y.id)[1]
        self.canvas.coords(self.id, x - 3, y - 3, x + 3, y + 3)

class Point(Item):
    
    def __init__(self, canvas, x, y, z):
        Item.__init__(self, canvas.items, "P", None)
        self.canvas = canvas
        self.x = x
        self.y = y
        self.z = z
        x.fellows.update({self.tag:self})
        y.fellows.update({self.tag:self})
        z.fellows.update({self.tag:self})
        self.spaces = []
        
    def repaint(self):
        for s in self.spaces:
            s.repaint()

    def new_visual(self, x, y):
        self.spaces.append(_Point(self.canvas, self, x, y))
        
