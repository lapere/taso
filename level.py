from Tkinter import *
from fellow import *
from item import Item       

class Level(Item):
    def __init__(self, canvas, value, typ):
        Item.__init__(self, canvas, typ)
        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="")
        self.selected_fill = dict(fill="green")
        if self.tag[0] == "X":
            self.line_list_param = [value, 0, value, canvas["height"]]
        else:
            self.y = value
            self.line_list_param = [0, value, canvas["width"], value]
        self.line_kw_param = dict(width=1, fill="gray", tags=self.tag)
        self.fun = str(value)
        self.create_visibles()
        

    def create_visibles(self):
        self.id = self.canvas.create_line(self.line_list_param,
                                          self.line_kw_param)
        self.canvas.tag_lower(self.tag)
        self.bindit()
        return self.id

    def repaint(self):
        pass

    def mouse_push(self, event):
        #self.fun = raw_input("anna kaava :")
        for g in globals():
            if g[0] == "X":
                print g
        
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

    #def repaint(self):
    #    self.canvas.coords(self.tag, self.x, 0, self.x, self.canvas["height"])  

    def __call__(self, x=None):
        if x:
            self.canvas.coords(self.id, x, 0, x, self.canvas["height"])
        else:
            return self.canvas.coords(self.id)[0]
   
    def recu(self, last, dx, dy):
          pass

class _Y(Level):

    def __init__(self, canvas, value):
        Level.__init__(self, canvas, value, "Y")

    #def repaint(self):
    #    self.canvas.coords(self.tag, 0, self.y, self.canvas["width"], self.y)

    def __call__(self, y=None):
        if y:
            self.canvas.coords(self.id, 0, y, self.canvas["width"], y)
        else:
            return self.canvas.coords(self.id)[1]
   
    def recu(self, last, dx, dy):
        pass
