"""       
class Level:

    cnt = 0

    def __init__(self, name, value):
        self.tag = name + str(Level.cnt)
        Level.cnt = Level.cnt + 1
        self.value = value
    
"""
from item import *

class _X(Item):

    def __init__(self, value, canvas):
        Item.__init__(self, canvas, "X")
        self.x = value

    def __call__(self, value = None):
        for fell in self.fellows:
            return self.canvas.coords(fell)[0]
        
   
class _Y(Item):

    def __init__(self, value, canvas):
        Item.__init__(self, canvas, "Y")
        self.y = value

    def __call__(self, value = None):
        for fell in self.fellows:
            return self.canvas.coords(fell)[1]
     
