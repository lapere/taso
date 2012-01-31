from Tkinter import *
from fellow import *
from item import *

class Line(Item):

    def __init__(self, canvas, startp, endp, style = dict(width=2)):
        Item.__init__(self, canvas, "L")

        self.org_x = startp.x.x
        self.org_y = startp.y.y

        self.startp = startp
        self.endp = endp
        
        self.x0 = startp.x
        self.y0 = startp.y
        self.x1 = endp.x
        self.y1 = endp.y

        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="black")
        self.selected_fill = dict(fill="green")
        self.style = style
        
        self.new_fellow(startp)
        self.new_fellow(endp)
        
        startp.new_fellow(self, other_end = endp)
        endp.new_fellow(self, other_end = startp)

        self.create_visibles()
        

    def create_visibles(self):
        
        self.style.update(dict(tags=self.tag))
            
        self.id = self.canvas.create_line(self.x0.x,
                                          self.y0.y,
                                          self.x1.x,
                                          self.y1.y,
                                          self.style)
        
        #Point must be above line for mouse_enter event
        self.canvas.tag_raise(self.startp.tag, self.tag)
        self.canvas.tag_raise(self.endp.tag, self.tag)
        
        self.endp.hidden()
        self.startp.hidden()

        self.canvas.tag_bind(self.tag, "<B1-Motion>", self.move)

        self.bindit()

        return self.id
    
    def move(self, event=None):
      
        if event:
            dx = event.x - self.org_x
            dy = event.y - self.org_y

            self.x0.x = self.x0.x + dx
            self.y0.y = self.y0.y + dy

            if self.x0 != self.x1:
                self.x1.x = self.x1.x + dx

            if self.y0 != self.y1:
                self.y1.y = self.y1.y + dy
            
        
            
        self.org_x = event.x
        self.org_y = event.y

        self.canvas.repaint()        
    
    def repaint(self):
        self.get_ends()
        self.canvas.coords(self.tag, self.x0.x, self.y0.y, self.x1.x, self.y1.y)  
    

    def get_ends(self):
        p = []
        for tag in self.fellows:
            p.append(self.fellows[tag])

        self.x0 = p[0].x
        self.y0 = p[0].y
        self.x1 = p[1].x
        self.y1 = p[1].y

        return p[0], p[1]
        

    def delete(self):
        pn = self.get_ends()
        for p in pn:
            p.fellows.pop(self.tag)
        self.canvas.delete(self.tag)
        
   
