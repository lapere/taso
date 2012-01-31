from Tkinter import *
from fellow import *
from item import Item

class Element(Item):

    def __init__(self, canvas, typ):
        Item.__init__(self, canvas, "E")
        self.typ = typ
        self.x = None
        self.y = None
        self.double_dim = False
        
    def create_visibles(self):
        return 0

    def repaint(self):
        for fell in self.fellows:
            self.fellows[fell].repaint()
        
    def new_fellow(self, fellow, other_end = None):
        if self.typ == 'x':
            if not self.x:
                self.x = fellow.x
            
            fellow.x = self.x

        elif self.typ == 'y':
            if not self.y:
                self.y = fellow.y
            
            fellow.y = self.y

        elif self.typ == 'angled':
            pass
        #self.canvas.repaint()
            
        if fellow.tag[0] == 'P':
            self.fellows.new_fellow(fellow, other_end)
            fellow.new_fellow(self)

        if fellow.tag[0] == 'D':
            self.fellows.new_fellow(fellow, other_end)
            
            
    def recu(self, last, dx, dy):
        #if self.double_dim:
        #    print "!Kaksois mitoitus", last
        #else: 
            if self.typ == 'x':
                self.x.x = self.x.x + dx
            if self.typ == 'y':
                self.y.y = self.y.y + dy

            self.double_dim=True

            for fell in self.fellows:
                if (fell[0] == 'D') and (fell != last):
                    d = self.fellows[fell]
                    if self.typ == d.typ:
                        d.recu(self.tag, dx, dy)
