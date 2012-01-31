from Tkinter import *
from line import *
from item import *

class Point(Item):
    
    def __init__(self, canvas, x, y):
        Item.__init__(self, canvas, "P")
        
        self.x = x()
        self.y = y()

        
        self.active_fill = dict(fill="red", outline="black")
        self.passive_fill = dict(fill="gray", outline="black")
        self.selected_fill = dict(fill="green", outline="black")

        self.create_visibles()
        
    def create_visibles(self):
        x = self.x
        y = self.y
        self.id = self.canvas.create_rectangle(x - 3, y - 3, x + 3, y + 3,
                                               fill="",
                                               outline="black",
                                               tags=self.tag)
        
        self.bindit()
        
        self.canvas.tag_bind(self.tag, "<B1-Motion>", self.move)
        #self.canvas.tag_bind(self.tag, "<ButtonRelease-1>", self.join)
        self.canvas.repaint()
        return self.id

        
    def move(self, event):
        
        x = int(self.canvasx(event.x))
        y = int(self.canvasy(event.y))
        
        if not self.x.names: 
            if self.x.tag[0] == "X":
                self.x.new_formula(str(x))
            elif self.x.tag[0] == "Y":
                self.x.new_formula(str(y))
        if not self.y.names: 
            if self.y.tag[0] == "Y":
                self.y.new_formula(str(y))
            elif self.y.tag[0] == "X":
                self.y.new_formula(str(x))

        self.canvas.repaint()
        
    def repaint(self):
        x, y = self.x.solve_line(self.y)
        self.canvas.coords(self.tag, x - 3, y - 3, x + 3, y + 3)

    def get_x(self):
        return self.canvas.coords(self.tag)[0] + 3

    def get_y(self):
        return self.canvas.coords(self.tag)[1] + 3 

    def join(self, event):
             
        o_point = self.find_overlapping_point(event)
 
        if o_point:

            print "Point.join" + "-" * (80-len("Point.join"))
            print "join", self.tag , "to", o_point.tag

            if o_point.tag[0] == "P":    
                lines = o_point.has_lines()
                if lines:
                    for line in lines:
                        line.fellows.pop(o_point.tag)
                        if line.startp == o_point:
                            line.startp = self    
                        else:
                            line.endp = self
                        line.new_fellow(self)
                        
                    for line in lines:
                        if line.startp == line.endp:
                            self.fellows.pop(line.tag)
                            self.canvas._delete(line)
                            
                    
                self.x.join(o_point.x)
                self.y.join(o_point.y)

                o_point.kill_fellows()
                self.canvas._delete(o_point)

            elif o_point.tag[0] == "X":
                self.x.join(o_point)
            elif o_point.tag[0] == "Y":
                self.y.join(o_point)
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
                elif tagg[0] == 'X':
                    x = self.canvas.items[tagg]
                    if x != self.x:
                        return x
                elif tagg[0] == 'Y':
                    y = self.canvas.items[tagg]
                    if y != self.y:
                        return y
        return None
                    

   
    def get_line_style(self, point):   
        lines = point.fellows

        for line_tag in lines:
            if line_tag[0] == 'L':
                style = lines[line_tag].style
                return style

    def has_lines(self):
        l = []
        for fell in self.fellows:
            if fell[0] == "L":
                l.append(self.fellows[fell])
        return l

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
    
            
    def hidden(self):
        self.passive_fill.update(dict(outline="", fill=""))
        self.passive_color()

