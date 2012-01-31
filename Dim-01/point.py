from Tkinter import *
from fellow import *
from item import *
from line import *

class Point(Item):
    
    def __init__(self, canvas, x, y):
        Item.__init__(self, canvas, "P")
    
        self.x = x 
        self.y = y
        self.active_fill = dict(fill="red", outline="black")
        self.passive_fill = dict(fill="", outline="black")
        self.selected_fill = dict(fill="green", outline="black")
        self.create_visibles()
        
    

    def create_visibles(self):
        x = self.x
        y = self.y
        self.id = self.canvas.create_rectangle(x.x - 3, y.y - 3, x.x + 3, y.y + 3,
                                               fill="",
                                               outline="black",
                                               tags=self.tag)
        
        self.canvas.tag_bind(self.tag, "<B1-Motion>", self.move)
        self.canvas.tag_bind(self.tag, "<ButtonRelease-1>", self.join)

        self.bindit()

        return self.id
           
    def move_fellows(self, dx = None, dy=None):
        ret = False
        for fell in self.fellows:
                if fell[0] == 'E':
                    if self.fellows[fell].typ == "x":
                        self.fellows[fell].recu(None, dx, 0)
                        ret = "x"
                    elif self.fellows[fell].typ == "y":
                        self.fellows[fell].recu(None, 0, dy)
                        ret = "y"
        return ret
        
    def move(self, event):
        self.move_fellows(event.x - self.x.x, event.y - self.y.y)
        self.x.x = event.x
        self.y.y = event.y 
                
        self.canvas.repaint()
        
    def repaint(self):
        self.canvas.coords(self.tag, self.x.x - 3, self.y.y - 3,
                                   self.x.x + 3, self.y.y + 3)

    def new_fellow(self, fellow, other_end = None):
        self.fellows.new_fellow(fellow, other_end)

        if fellow.tag[0] == 'E':
            for fell in self.fellows:
                if fell[0] == 'D':
                    fellow.new_fellow(self.fellows[fell])
                    self.fellows[fell].new_fellow(fellow)
                if fell[0] == 'L':
                    self.canvas.tag_unbind(fell, "<B1-Motion>")


    def join(self, event):
        
        o_point = self.find_overlapping_point(event)
        
        if o_point:
            print "Point.join" + "-" * (80-len("Point.join"))
            print "join", self.tag , "to", o_point.tag
            if o_point.has_lines():
                style = self.get_line_style(o_point)
                ends = self.steal_overlapping_line_ends(o_point)
                ends = ends + self.steal_overlapping_line_ends(self)
                self.fellows.clear()
                ends = set(ends)
              
                for end in ends:
                    if self.tag != end.tag:
                        Line(self.canvas, startp=self, endp=end, style=style)

        
            for e in o_point.fellows:
                if e[0] == 'E':
                    ele = o_point.fellows[e]
                    self_ele = self.has_elements()
                    for n in  self_ele:
                        self.canvas.join_elements(ele, n)
                    
                    ele.new_fellow(self)
                    ele.fellows.pop(o_point.tag)
                    
                    
            self.canvas.items.pop(o_point.tag)
            self.canvas.delete(o_point.tag)
            print "-" * 80 


    def find_overlapping_point(self, event):

        t = self.canvas.find_overlapping(event.x - 1,
                                         event.y - 1,
                                         event.x + 1,
                                         event.y + 1)
        
        for c in self.canvas.gettags(CURRENT):
            if c[0] == 'P':
                curr = c
        
        for tag in t:
            for tagg in self.canvas.gettags(tag):

                if tagg[0] == 'P':
                    point = self.canvas.items[tagg]
            
                    if tagg != curr:
                        return point

    def get_line_style(self, point):   
        lines = point.fellows

        for line_tag in lines:
            if line_tag[0] == 'L':
                style = lines[line_tag].style
                return style

    def has_lines(self):
        for fell in self.fellows:
            if fell[0] == "L":
                return True
        return False

    def has_elements(self):
        e = []
        for fell in self.fellows:
            if fell[0] == "E":
                e.append(self.fellows[fell])
        return e

    def steal_overlapping_line_ends(self, point):

        Points = []

        lines = point.fellows

        for line_tag in lines:
            if line_tag[0] == 'L':
                print "delete", line_tag
                endp = lines.get_endpoint(line_tag)
                Points.append(endp)
            
                self.canvas.items.pop(line_tag)
                endp.fellows.pop(line_tag)
                #self.fellows.pop(line_tag)
                self.canvas.delete(line_tag)
        
        return Points
    

    def delete(self):
        l = []

        for fell in self.fellows:
            l.append(self.fellows[fell])

        for fell in l:
            if fell.tag == 'E':
                fell.fellows.pop(self.tag)
            elif fell.tag == 'L':
                fell.delete()
                self.canvas.items.pop(fell.tag)

        self.canvas.delete(self.tag)
                
    def elements(self):
        e = []
        for fell in self.fellows:
            if fell[0] == 'E':
                e.append(self.fellows[fell])
        return e

    def hidden(self):
        self.passive_fill.update(dict(outline="", fill=""))
        self.passive_color()

