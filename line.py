from Tkinter import *
from fellow import *
from cad_kernel import *
from cad_kernel.utils import *

class Line(Item):

    def __init__(self, canvas, startp, endp, style = dict(width=2)):
        Item.__init__(self, canvas, "L")

        self.org_x = startp.x()
        self.org_y = startp.y()

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

        
        l = DistBetweenTwoPoint(self.startp.x(),
                                self.startp.y(), 
                                self.endp.x(),
                                self.endp.y())
        
        self.canvas.S[self.tag] = Formula(str(l))        

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

        if not self.endp.elements() and not self.startp.elements(): 
            pass
            #self.canvas.tag_bind(self.tag, "<B1-Motion>", self.move)

        self.bindit()
        self.canvas.repaint()
        return self.id
    
    def move(self, event):
    
        dx = self.canvasx(event.x) - self.org_x
        dy = self.canvasy(event.y) - self.org_y
         
        self.startp.x(self.startp.x() + dx)
        self.startp.y(self.startp.y() + dy)        
        
        if self.typ() != "x":
            self.endp.x(self.endp.x() + dx)
        if self.typ() != "y":
            self.endp.y(self.endp.y() + dy)
                                            
        self.org_x = self.canvasx(event.x)
        self.org_y = self.canvasy(event.y)

        self.canvas.repaint()        

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
        
    def delete(self):
        pn = self.get_ends()
        for p in pn:
            p.fellows.pop(self.tag)
        self.canvas.delete(self.tag)

class Dimension(Line):

    def __init__(self, canvas, startp, endp):
        style = dict(width=1, arrow=BOTH, arrowshape=(16,16,2))
        
        
        self.txtx = (startp.get_x() + endp.get_x()) / 2
        self.txty = (startp.get_y() + endp.get_y()) / 2

        self.txt = StringVar()
        self._txt_e = Entry(canvas, width=3, bg="white" ,
                            disabledbackground = "white",
                            relief=FLAT, bd=0, textvariable=self.txt,
                            state=DISABLED)
        
        self._txt_id = canvas.create_window(self.txtx, self.txtx,
                                                window=self._txt_e)
        
        Line.__init__(self, canvas, startp, endp, style)
        
    def repaint(self):
       
        self.canvas.coords(self.tag, self.startp.get_x(),
                                     self.startp.get_y(),
                                     self.endp.get_x(),
                                     self.endp.get_y())  
    
        self.txtx = (self.startp.get_x() + self.endp.get_x()) / 2
        self.txty = (self.startp.get_y() + self.endp.get_y()) / 2
        
        
        self.canvas.coords(self._txt_id, self.txtx, self.txty)
        val = self.canvas.S[self.tag].value
        self.txt.set(val)