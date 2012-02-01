from Tkinter import *
from item import *   
from utils import *


class XSpace(VisualItem):

    def __init__(self, canvas, x0, x1):
        VisualItem.__init__(self, canvas, "S", None)
        self.line_list_param = [int(x0), 100, int(x1), 100]
        self.x0 = x0
        self.x1 = x1
        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="black")
        self.selected_fill = dict(fill="green")
        self.hidden_fill = dict(fill="")            

        self.line_kw_param = dict(width=1, fill="gray", tags=self.tag, arrow=LAST)
        self.create_visibles()
        
        ids = self.canvas.find_overlapping (float(self.x0), 0,
                                            float(self.x1),
                                            self.canvas["height"])
        for i in ids:
            tag = self.canvas.gettags(i)[0]
            coord = self.canvas.coords(tag)
            coord = [coord[0] + 200, coord[1], coord[2] + 200, coord[3]]
            c = copy.copy(self.canvas.items[tag])
            c.canvas = self.canvas
            #i = c.create_visibles()
            self.canvas.coords(c.id,coord[0],
                               coord[1],
                               coord[2],
                               coord[3])          

    def create_visibles(self):
        
        self.id = self.canvas.create_line(self.line_list_param,
                                          self.line_kw_param)
        self.canvas.tag_lower(self.tag)
        
        self.bindit()
        return self.id

    def repaint(self):
        pass
    
