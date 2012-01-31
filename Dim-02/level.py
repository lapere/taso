from Tkinter import *
from fellow import *
from item import Item       

class Level(Item):
    def __init__(self, canvas, value, typ):
        Item.__init__(self, canvas, typ)
        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="gray")
        self.selected_fill = dict(fill="green")
        if self.tag[0] == "X":
            self.x = value
            self.line_list_param = [self.x, 0, self.x, canvas["height"]]
        else:
            self.y = value
            self.line_list_param = [0, self.y, canvas["width"], self.y]
        self.line_kw_param = dict(width=1, fill="gray", tags=self.tag)
        self.create_visibles()


    def create_visibles(self):
        self.id = self.canvas.create_line(self.line_list_param,
                                          self.line_kw_param)
        self.bindit()
        return self.id
    
    def repaint(self):
        self.canvas.coords([self.tag] + self.line_list_param)  

    def new_fellow(self, fellow, other_end = None):

        if self.tag[0] == "X":
            fellow.x = self
        else:
            fellow.y = self

        if fellow.tag[0] == 'P':
            self.fellows.new_fellow(fellow, other_end)
            #fellow.new_fellow(self)

        if fellow.tag[0] == 'D':
            self.fellows.new_fellow(fellow, other_end)

    def join(self, other):
        for fell in other.fellows:
            o = other.fellows[fell]    
            self.new_fellow(o)
        
    
class _X(Level):

    def __init__(self, canvas, value):
        Level.__init__(self, canvas, value, "X")

    def repaint(self):
        self.canvas.coords(self.tag, self.x, 0, self.x, self.canvas["height"])  
            
    def recu(self, last, dx, dy):
        #if self.double_dim:
        #    print "!Kaksois mitoitus", last
        #else: 
            
            self.x.x = self.x.x + dx
            self.double_dim=True

            for fell in self.fellows:
                if (fell[0] == 'D') and (fell != last):
                    d = self.fellows[fell]
                    if self.typ == d.typ:
                        d.recu(self.tag, dx, dy)

class _Y(Level):

    def __init__(self, canvas, value):
        Level.__init__(self, canvas, value, "Y")

    def repaint(self):
        self.canvas.coords(self.tag, 0, self.y, self.canvas["width"], self.y)
        
    def recu(self, last, dx, dy):
        #if self.double_dim:
        #    print "!Kaksois mitoitus", last
        #else: 
            
            self.y.y = self.y.y + dy
            self.double_dim=True

            for fell in self.fellows:
                if (fell[0] == 'D') and (fell != last):
                    d = self.fellows[fell]
                    if self.typ == d.typ:
                        d.recu(self.tag, dx, dy)

     
