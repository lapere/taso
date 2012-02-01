from Tkinter import *
from fellow import *
from item import *
from line import *
from level import _X,_Y 

class Point(Item):
    
    def __init__(self, canvas, x, y):
        Item.__init__(self, canvas, "P")

        self.x = x 
        self.y = y

        self.active_fill = dict(fill="red", outline="black")
        self.passive_fill = dict(fill="", outline="black")
        self.selected_fill = dict(fill="green", outline="black")
        self.create_visibles()
        
        self.x.new_fellow(self)
        self.y.new_fellow(self)

        self.new_fellow(x)
        self.new_fellow(y)

    def create_visibles(self):
        x,y = self.solve_line_line(self.x, self.y)
        
        self.id = self.canvas.create_rectangle(x - 3, y - 3, x + 3, y + 3,
                                               fill="",
                                               outline="black",
                                               tags=self.tag)
        
        self.bindit()
        
        self.canvas.tag_bind(self.tag, "<B1-Motion>", self.move)
        self.canvas.tag_bind(self.tag, "<ButtonRelease-1>", self.join)

        return self.id
           
    def move_fellows(self, dx = None, dy=None):
        for fell in self.fellows:
            self.fellows[fell].recu(None, dx, dy)
            
    def move(self, event):
        
        x = int(self.canvasx(event.x))
        y = int(self.canvasy(event.y))

        for fell in self.fellows:
            self.fellows[fell].set_end(x, y)
        
        #self.move_fellows(x - self.x.get_x(), y - self.y.get_y())
        #self.x.set(x,y)
        #self.y.set(x,y)
                                   
        self.canvas.repaint()
        
    def get_x(self):
        return self.x.get_x()

    def get_y(self):
        return self.y.get_y()
    
    def repaint(self):
        
        a = []

        for fell in self.fellows:
            if fell[0] == "A":
                a.append(self.fellows[fell])

        if len(a) == 1:
            x,y = self.solve_line_line(self.y, a[0])
            if x != 0 and y != 0: 
                self.canvas.coords(self.tag, x - 3, y - 3, x + 3, y + 3)
            x,y = self.solve_line_line(self.x, a[0])
            if x == 0 and y == 0:
                x,y = self.x.get_x(), self.y.get_y()
        elif len(a) == 2:
            x,y = self.solve_line_line(a[0], a[1])
        else:
            x,y = self.x.get_x(), self.y.get_y()
            
        self.canvas.coords(self.tag, x - 3, y - 3, x + 3, y + 3)

    def new_fellow(self, fellow, other_end = None):
        self.fellows.new_fellow(fellow, other_end)

                
    def solve_line_line(self, l1, l2):
        #print l1,l2
        
        nim = l1.A() * l2.B() - l2.A() * l1.B()

        if not nim:
            return 0, 0
            
        x_os = -l1.C() *  l2.B() - -l2.C() *  l1.B()
        y_os =  l1.A() * -l2.C() - l2.A() * -l1.C()

        x = float(x_os) / nim
        y = float(y_os) / nim
    
        return x, y
    
    
    def join(self, event):
        return     
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

    def delete(self, event):
        self.canvas.items.pop(self.tag)
        self.canvas.delete(self.tag)
        self.canvas.unbind("<Button-3>")
        self.canvas.unbind("<Motion>")

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
    

    def kill_fellows(self):
        self.x.fellows.pop(self.tag)
        self.y.fellows.pop(self.tag)
            
                
    def elements(self):
        e = []
        for fell in self.fellows:
            if fell[0] == 'E':
                e.append(self.fellows[fell])
        return e

    def hidden(self):
        self.passive_fill.update(dict(outline="", fill=""))
        self.passive_color()

