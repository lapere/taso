from Tkinter import *
from item import VisualItem     
from utils import *


class Txt(VisualItem):

    def __init__(self, canvas, p, value=None):
        VisualItem.__init__(self, canvas, "T", value)
        
        self.p = p

        p.fellows.update({self.tag:self})
        
        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="black")
        self.selected_fill = dict(fill="green")
        self.hidden_fill = dict(fill="")

        x,y = self.p.value
        self.list_param = [x, y]
        self.kw_param = dict(tags=self.tag, text=str(self.value), anchor=S)

        self.create_visibles()
        
                
    def create_visibles(self):
        
        self.id = self.canvas.create_text(self.list_param,
                                          self.kw_param)
        self.canvas.tag_lower(self.tag)
        self.bindit()
        return self.id

    def repaint(self):
        x,y = self.p.value
        self.canvas.itemconfig(self.tag, text=str(self))
        self.canvas.coords(self.tag, x, y)

