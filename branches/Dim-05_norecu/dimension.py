from Tkinter import *
from fellow import *
from level import _X, _Y
from utils import *
from item import *

class Dimension(Item):
    

    def __init__(self, canvas, elements, typ):
        Item.__init__(self, canvas, "D")
        
        self.typ = typ
        self.double_dim = False
        #save only elements tags for pickle
        self.elements = elements[0].tag, elements[1].tag 
        self.fun = ""
        min_x = 20000
        min_y = 20000

        for e in elements:
            for fell in e.fellows:
                if fell[0] == 'P':
                    p = e.fellows[fell]
                    min_x = min(min_x, p.x())
                    min_y = min(min_y, p.y())
            self.new_fellow(e)
            e.new_fellow(self)
    
        if self.typ == "X":
            y = _Y(self.canvas, min_y - 25)
            startp = self.canvas.point(elements[0], y)
            endp = self.canvas.point(elements[1], y)
            self.line = self.canvas.line(startp, endp)
        else:
            x = _X(self.canvas, min_x - 25)
            startp = self.canvas.point(x, elements[0])
            endp = self.canvas.point(x, elements[1])
            self.line = self.canvas.line(startp, endp)


        self.line.style = dict(width=1, arrow=BOTH, arrowshape=(16,16,2))
        elements[0].new_fellow(startp)
        elements[1].new_fellow(endp)
            
        self.line.addtag(self.tag)

        startp, endp  = self.line.get_ends()
        startp.new_fellow(self)
        endp.new_fellow(self)
        
        self.create_visibles()
        
    def mouse_push(self, event):
        self.fun = raw_input("anna kaava :")   

    def create_visibles(self):  

        self.value = StringVar(self.canvas)
        
        self.txtx = (self.line.startp.x() + self.line.endp.x()) / 2
        self.txty = (self.line.startp.y() + self.line.endp.y()) / 2

    
        self.e = Entry(self.canvas, width=3, bg="white",
                       relief=FLAT, bd=0, textvariable=self.value)
        
        self.e.bind("<KeyPress>", self.g)

        self.id_txt = self.canvas.create_window(self.txtx, self.txty,
                                                window=self.e, tags=self.tag)

        self.canvas.itemconfig(self.line.id, width=1, arrow=BOTH, arrowshape=(16,16,2))
        l = DistBetweenTwoPoint(self.line.startp.x(),
                                self.line.startp.y(), 
                                self.line.endp.x(),
                                self.line.endp.y())
        
        #self.canvas.coords(self.id_txt, self.txtx, self.txty)
        self.value.set(str(int(round(l))))
        self.e['width'] = len(self.value.get())
    
        return self.id_txt

    def move_recu(self):
        pass
        
    def g(self, event):
        if event.keysym == "Return":
            val = float(self.value.get())
            self.canvas.repaint()
            self.canvas.focus_set()
                
    def recu(self, last, dx, dy):
        pass    

    def repaint(self):
        #self.move_recu()
        self.line.get_ends()
        self.txtx = (self.line.startp.x() + self.line.endp.x()) / 2
        self.txty = (self.line.startp.y() + self.line.endp.y()) / 2
        #l = DistBetweenTwoPoint(self.line.startp.x(),
        #                        self.line.startp.y(), 
        #                        self.line.endp.x(),
        #                        self.line.endp.y())
        
        self.canvas.coords(self.id_txt, self.txtx, self.txty)
        #self.value.set(str(int(round(l))))
        #self.e['width'] = len(self.value.get())


    def get_elements(self):
        e = []
        for fell in self.fellows:
            if fell[0] == self.typ:
                e.append(self.fellows[fell])

        return e


