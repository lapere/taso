from Tkinter import *
from line import *
from item import *
import level

class Selection(VisualItem):
    
    def __init__(self, canvas, points):
        VisualItem.__init__(self, canvas, "S", None)

        self.points = points
        self.x_list = []
        self.y_list = []
        for p in points:
            p.fellows.update({self.tag:self})
            #self.coord_list.append(p.x)
            #self.coord_list.append(p.y)
            self.fellows.update({p.x.tag:p.x, p.y.tag:p.y}) 
            self.x_list.append(p.x)
            self.y_list.append(p.y)
            
        self.active_fill = dict(fill="red", outline="black")
        self.passive_fill = dict(fill="", outline="")
        self.selected_fill = dict(fill="green", outline="black")
        self.hidden_fill = dict(fill="", outline="")            

        self.style = dict(current.selection_style)
        self.create_visibles()
        
    def create_visibles(self):
        self.style.update(dict(tags=self.tag))
        #c_l = map(lambda x:x*self.canvas._scale, self.coord_list)
                
        self.id = self.canvas.create_rectangle(0, 0, 0, 0, self.style)
        
        if not self.visible:
            self.hide()
            
        self.bindit()
        self.canvas.tag_bind(self.tag, "<B1-Motion>", self.move)
        self.repaint()
        return self.id

    def move(self, event):
        
        dx = (self.canvas.canvasx(event.x) - self.org_x) / self.canvas._scale
        dy = (self.canvas.canvasy(event.y) - self.org_y) / self.canvas._scale

        for f in self.fellows:
            i = self.fellows[f]
            if f[0] == "X":
                i.new_formula(str(i + dx))
            elif f[0] == "Y":
                i.new_formula(str(i + dy))
                                         
        self.org_x = self.canvas.canvasx(event.x)
        self.org_y = self.canvas.canvasy(event.y)
        
        self.canvas.repaint()        
    
    def repaint(self):
        x0 = min(map(lambda x:x*self.canvas._scale - 15, self.x_list))
        y0 = min(map(lambda x:x*self.canvas._scale - 15, self.y_list))
        x1 = max(map(lambda x:x*self.canvas._scale + 15, self.x_list))
        y1 = max(map(lambda x:x*self.canvas._scale + 15, self.y_list))
        
        self.canvas.coords(self.tag, x0, y0, x1, y1)
