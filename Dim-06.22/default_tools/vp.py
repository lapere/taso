from Tkinter import *
from item import *   
from utils import *
import copy


class VisualPrimitive:

    def __init__(self, canvas, value, offset):
        self.value = value
        self.offset = offset
        self.canvas = canvas
        
        self.selected = False
        self.visible = True
        
    def create_visibles(self):
        self.id = self.canvas.create_line(self.list_param,
                                          self.kw_param)
        #self.canvas.visuals[self.id] = self
        self.bindit()
        self.repaint()
        return self.id   
                           
    def bindit(self):
        self.canvas.tag_bind(self.id, "<Button-1>", self.mouse_push)
        self.canvas.tag_bind(self.id, "<Shift-Button-1>", self.mouse_select)
        self.canvas.tag_bind(self.id, "<Enter>", self.mouse_enter)
        self.canvas.tag_bind(self.id, "<Leave>", self.mouse_leave)
        self.canvas.tag_bind(self.id, "<Double-Button-1>", self.mouse_double)
        self.canvas.tag_bind(self.id, "<Double-Button-3>", self.print_status)

    def unbind(self):
        self.canvas.tag_unbind(self.id, "<Button-1>")
        self.canvas.tag_unbind(self.id, "<Shift-Button-1>")
        self.canvas.tag_unbind(self.id, "<Enter>")
        self.canvas.tag_unbind(self.id, "<Leave>")
        self.canvas.tag_unbind(self.id, "<Double-Button-1>")
        self.canvas.tag_unbind(self.id, "<Double-Button-3>")

    def mouse_enter(self, event):
        if isinstance(self, Point):
            self.canvas.tag_raise(self.id)
        self.active_color()

    def mouse_leave(self, event):
        self.passive_color()

    def mouse_push(self, event):
        self.org_x = self.canvas.canvasx(event.x)
        self.org_y = self.canvas.canvasy(event.y)
        self.e_copy()
        self.canvas.e.icursor(END)
        self.canvas.e['width'] = len(self.canvas.cmd.get()) + 1
        self.canvas.update()

    def e_copy(self):
        self.canvas.cmd.set(self.canvas.cmd.get() + str(self.value))
        
    def entry_set(self):
        self.canvas.cmd.set(str(self.value))

    def entry_get(self):
        self.value = eval(self.canvas.cmd.get())
        
    def mouse_double(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.entry_set()
        self.canvas.e.bind("<KeyPress>", self.g)
        self.id_txt = self.canvas.create_window(x, y, window=self.canvas.e)
        
    def g(self, event):
        self.canvas.e['width'] = len(self.canvas.cmd.get()) + 1
        if event.keysym == "Return":
            self.entry_get()
            #self.canvas.repaint()
            self.repaint()
            self.canvas.delete(self.id_txt)
            self.canvas.focus_set()
            
        
    def mouse_select(self, event):
        if self.value.visible:
            self.value.visible = False
            self.hide()
        else:
            self.value.visible = True
            self.unhide()
            
    def repaint(self):
        pass
        
    def active_color(self):
        self.canvas.itemconfig(self.id, self.active_fill)

    def passive_color(self):
        self.canvas.itemconfig(self.id, self.passive_fill)

    def selected_color(self):
        self.canvas.itemconfig(self.id, self.value.selected_fill)
        

    def hide(self, event=None):
        self.unbind()
        self.canvas.itemconfig(self.id, self.hidden_fill)
        
    def unhide(self):
        self.bindit()
        self.canvas.itemconfig(self.id, self.passive_fill)
        
    def delete(self):
        for fell in self.fellows:
            f = self.fellows[fell]
            if f.fellows.has_key(self.id): 
                f.fellows.pop(self.id)
            f.delete()
        self.canvas.delete(self.id)
        if self.canvas.items.has_key(self.id):
            del self.canvas.items[self.id]      
                
    def addtag(self, tag):
        self.canvas.addtag_withtag(tag, self.id)

    
    def __call__(self):
        try:
            return float(self)
        except:
            return None
    
    def __getstate__(self):
        odict = self.__dict__.copy() # copy the dict since we change it    
        odict['canvas'] = None
        odict['code'] = None
        
        return odict

    
    def __setstate__(self, dicti):
        if dicti:
            self.__dict__.update(dicti)   # update attributes
        
    
    def print_status(self, event=None):
        print self.id,"(",self.id,") =", self.value


#-------------------------------------------------------------------------------

class VerticalLine(VisualPrimitive):

    def __init__(self, canvas, value, offset):
        VisualPrimitive.__init__(self, canvas, value, offset)
        
        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="gray")
        self.selected_fill = dict(fill="green")
        self.hidden_fill = dict(fill="")            

        self.kw_param = dict(width=1, fill="gray")
        self.list_param = [self.value, 0, self.value, self.canvas["height"]]

        self.create_visibles()
  
        self.canvas.tag_lower(self.id)
        self.canvas.tag_bind(self.id, "<B1-Motion>", self.move)
    

    def repaint(self):
        s = self.canvas._scale
        self.canvas.coords(self.id,
                           self.offset + self.value * s,
                           0,
                           self.offset + self.value * s,
                           self.canvas["height"])
                    
    def move(self, event):
        
        x = int(self.canvas.canvasx(event.x))
        s = self.canvas._scale
        self.value = x / s
        self.repaint()
        

#-------------------------------------------------------------------------------

class HorizontalLine(VisualPrimitive):

    def __init__(self, canvas, value, offset):
        VisualPrimitive.__init__(self, canvas, value, offset)
        self.offset = offset
        
        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="gray")
        self.selected_fill = dict(fill="green")
        self.hidden_fill = dict(fill="")            
        
        self.list_param = [0, self.value, canvas["width"], self.value]
        self.kw_param = dict(width=1, fill="gray")
        
        self.create_visibles()
    
        self.canvas.tag_lower(self.id)
        self.canvas.tag_bind(self.id, "<B1-Motion>", self.move)
    

    def repaint(self):
        s = self.canvas._scale
        self.canvas.coords(self.id,
                           0,
                           self.offset + self.value * s,
                           self.canvas["width"],
                           self.offset + self.value * s)
    def move(self, event):
        
        y = int(self.canvas.canvasx(event.y))
        s = self.canvas._scale
        self.value = y / s
        self.repaint()
    
#-------------------------------------------------------------------------------    

class AngledLine(VisualPrimitive):
    
    def __init__(self, canvas, x, y, a, offset):
        VisualPrimitive.__init__(self, canvas, (x,y,a), offset)

        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="gray")
        self.selected_fill = dict(fill="green")
        self.hidden_fill = dict(fill="")
        
        self.list_param = [0,100,200,300]
        self.kw_param = dict(width=1, fill="gray")

        self.create_visibles()
        self.repaint()
        self.canvas.tag_lower(self.id)
        self.canvas.tag_bind(self.id, "<B1-Motion>", self.move)

    def move(self, event):

        x = int(self.canvas.canvasx(event.x))
        y = int(self.canvas.canvasy(event.y))

        xx = self.value[0]
        yy = self.value[1]

        a =  RadBetweenTwoPoint(x,y,xx,yy)
        
        self.value = xx, yy, a
        
        self.repaint()
        
    def repaint(self):
        x, y, a = self.value
        _x = self.offset + float(x) * self.canvas._scale
        _y = self.offset + float(y) * self.canvas._scale

        if cos(a) and sin(a):
            l = [_x - cos(a) * 10,
                 _y + sin(a) * 10,
                 _x + cos(a) * 10,
                 _y - sin(a) * 10]
        elif not sin(a):
            l = [_x, _y - 10, _x, _y + 10]
        else:
            l = [_x - 10, _y, _x + 10, _y]
        m = float(max(self.canvas["width"], self.canvas["height"]))
        self.canvas.coords(self.id, l[0], l[1], l[2], l[3])        
        self.canvas.scale(self.id, _x, _y, m/10, m/10)
        
        
#-------------------------------------------------------------------------------

class Point(VisualPrimitive):

    def __init__(self, canvas, x, y, offset):
        VisualPrimitive.__init__(self, canvas, (x,y), offset)
        
        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="black")
        self.selected_fill = dict(fill="green")
        self.hidden_fill = dict(fill="", outline="")            

        self.list_param = [x, y, x, y]
        self.kw_param = dict(fill="black", width=7, capstyle = PROJECTING)
        
        self.create_visibles()

    def repaint(self):
        x, y = self.value
        self.canvas.coords(self.id, x, y, x, y)

#-------------------------------------------------------------------------------

class Line(VisualPrimitive):

    def __init__(self, canvas, x0, y0, x1, y1, offset):
        VisualPrimitive.__init__(self, canvas, (x0, y0, x1, y1), offset)
        
        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="black")
        self.selected_fill = dict(fill="green")
        self.hidden_fill = dict(fill="")

        self.list_param = list(self.value)
        self.kw_param = dict(fill="black", width=1)
        
        self.create_visibles()
        
        #Point must be above line for mouse_enter event
        self.canvas.tag_lower(self.id)
    
        
    def move(self, event):    
        pass
    
    def repaint(self):
        s = self.canvas._scale
        x0,y0,x1,y1 = self.value
        self.canvas.coords(self.id, x0*s, y0*s, x1*s, y1*s)                              
        #self.canvas.itemconfig(self.id, self.kw_param)
    
    def arrows(self):
        self.kw_param.update(dict(arrow=BOTH, arrowshape=(16,16,2)))
        self.canvas.itemconfig(self.id, arrow=BOTH, arrowshape=(16,16,2))

    def width(self, value):
        self.kw_param.update(dict(width=value))
        self.canvas.itemconfig(self.id, width=value)
