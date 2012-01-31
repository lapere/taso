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

        min_x = 20000
        min_y = 20000

        for e in elements:
            for fell in e.fellows:
                if fell[0] == 'P':
                    p = e.fellows[fell]
                    min_x = min(min_x, p.get_x())
                    min_y = min(min_y, p.get_y())
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
        
    def create_visibles(self):  

        self.value = StringVar(self.canvas)
        
        self.txtx = (self.line.startp.get_x() + self.line.endp.get_x()) / 2
        self.txty = (self.line.startp.get_y() + self.line.endp.get_y()) / 2

    
        self.e = Entry(self.canvas, width=3, bg="white",
                       relief=FLAT, bd=0, textvariable=self.value)
        
        self.e.bind("<KeyPress>", self.g)

        self.id_txt = self.canvas.create_window(self.txtx, self.txty,
                                                window=self.e, tags=self.tag)

        self.canvas.itemconfig(self.line.id, width=1, arrow=BOTH, arrowshape=(16,16,2))
        l = DistBetweenTwoPoint(self.line.startp.get_x(),
                                self.line.startp.get_y(), 
                                self.line.endp.get_x(),
                                self.line.endp.get_y())
        
        #self.canvas.coords(self.id_txt, self.txtx, self.txty)
        self.value.set(str(int(round(l))))
        self.e['width'] = len(self.value.get())
    
        return self.id_txt

    def move_recu(self):
        val = float(self.value.get())
        e = self.get_elements()

        if self.typ == "X":
            if e[0]() > e[1]():
                x = e[0]() - e[1]()
                dx = val - x
                e[0].recu(self.tag, dx, 0)
            else:
                x = e[1]() - e[0]()
                dx = val - x
                e[1].recu(self.tag, dx, 0)
            
        elif self.typ == "Y":
            if e[0]() > e[1]():
                y = e[0]() - e[1]()
                dy = val - y
                e[0].recu(self.tag, 0, dy)
            else:
                y = e[1]() - e[0]()
                dy = val - y
                e[1].recu(self.tag, 0, dy)
        
    def g(self, event):
        if event.keysym == "Return":    
            self.move_recu()
            for tag in self.canvas.items:
                i = self.canvas.items[tag]
                if tag[0] == 'E':
                    i.double_dim = False
                elif tag[0] == 'D':
                    i.double_dim = False
               
            self.canvas.repaint()
            self.canvas.focus_set()
                
    def recu(self, last, dx, dy):
        #if self.double_dim:
        #    print "!DD",self.tag
        #else:
        #    self.double_dim = True
            for fell in self.fellows:
                if (fell[0] == self.typ) and (fell != last):
                    e = self.fellows[fell]
                    if self.typ == fell[0]:
                        e.recu(self.tag, dx, dy)
            

    def repaint(self):
        #self.move_recu()
        self.line.get_ends()
        self.txtx = (self.line.startp.get_x() + self.line.endp.get_x()) / 2
        self.txty = (self.line.startp.get_y() + self.line.endp.get_y()) / 2
        #l = DistBetweenTwoPoint(self.line.startp.get_x(),
        #                        self.line.startp.get_y(), 
        #                        self.line.endp.get_x(),
        #                        self.line.endp.get_y())
        
        self.canvas.coords(self.id_txt, self.txtx, self.txty)
        #self.value.set(str(int(round(l))))
        #self.e['width'] = len(self.value.get())


    def get_elements(self):
        e = []
        for fell in self.fellows:
            if fell[0] == self.typ:
                e.append(self.fellows[fell])

        return e


