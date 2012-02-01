from Tkinter import *
from item import *   
from utils import *
import copy


class VisualPrimitive:

    def __init__(self, canvas, value):
        self.value = value
        self.tag = value.tag
        self.canvas = canvas
        
        self.selected = False
        self.visible = True
        
    def create_visibles(self):
        self.id = self.canvas.create_line(self.list_param,
                                          self.kw_param)
        self.canvas.visuals[self.id] = self
        self.bindit()
        return self.id   
                           
    def bindit(self):
        self.canvas.tag_bind(self.tag, "<Button-1>", self.mouse_push)
        self.canvas.tag_bind(self.tag, "<Shift-Button-1>", self.mouse_select)
        self.canvas.tag_bind(self.tag, "<Enter>", self.mouse_enter)
        self.canvas.tag_bind(self.tag, "<Leave>", self.mouse_leave)
        self.canvas.tag_bind(self.tag, "<Double-Button-1>", self.mouse_double)
        self.canvas.tag_bind(self.tag, "<Double-Button-3>", self.print_status)

    def unbind(self):
        self.canvas.tag_unbind(self.tag, "<Button-1>")
        self.canvas.tag_unbind(self.tag, "<Shift-Button-1>")
        self.canvas.tag_unbind(self.tag, "<Enter>")
        self.canvas.tag_unbind(self.tag, "<Leave>")
        self.canvas.tag_unbind(self.tag, "<Double-Button-1>")
        self.canvas.tag_unbind(self.tag, "<Double-Button-3>")

    def mouse_enter(self, event):
        if self.tag[0] == "P":
            self.canvas.tag_raise(self.tag)
            #self.repaint()
        self.active_color()

    def mouse_leave(self, event):
        self.passive_color()

    def mouse_push(self, event):
        self.org_x = self.canvas.canvasx(event.x)
        self.org_y = self.canvas.canvasy(event.y)
        self.canvas.cmd.set(self.canvas.cmd.get() + self.tag)
        self.canvas.e.icursor(END)
        self.canvas.e['width'] = len(self.canvas.cmd.get()) + 1
        self.canvas.update()
        
    def mouse_double(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.canvas.cmd.set(self.value.formula)
        self.canvas.e.bind("<KeyPress>", self.g)
        self.id_txt = self.canvas.create_window(x, y, window=self.canvas.e)
        
    def g(self, event):
        self.canvas.e['width'] = len(self.canvas.cmd.get()) + 1
        if event.keysym == "Return":
            self.value.new_formula(self.canvas.cmd.get())
            #self.canvas.items.recalc()
            self.canvas.repaint()
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
        self.canvas.itemconfig(self.tag, self.active_fill)

    def passive_color(self):
        self.canvas.itemconfig(self.tag, self.passive_fill)

    def selected_color(self):
        self.canvas.itemconfig(self.tag, self.value.selected_fill)
        

    def hide(self, event=None):
        self.unbind()
        self.canvas.itemconfig(self.tag, self.hidden_fill)
        
    def unhide(self):
        self.bindit()
        self.canvas.itemconfig(self.tag, self.passive_fill)
        
    def delete(self):
        for fell in self.fellows:
            f = self.fellows[fell]
            if f.fellows.has_key(self.tag): 
                f.fellows.pop(self.tag)
            f.delete()
        self.canvas.delete(self.tag)
        if self.canvas.items.has_key(self.tag):
            del self.canvas.items[self.tag]      
                
    def addtag(self, tag):
        self.canvas.addtag_withtag(tag, self.tag)

    
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
        print self.tag,"(",self.id,") =", self.value


#-------------------------------------------------------------------------------

class X(VisualPrimitive):

    def __init__(self, canvas, value, origo):
        VisualPrimitive.__init__(self, canvas, value)
        self.origo = origo
        
        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="gray")
        self.selected_fill = dict(fill="green")
        self.hidden_fill = dict(fill="")            

        self.kw_param = dict(width=1, fill="gray", tags=value.tag)
        self.list_param = [self.value, 0, self.value, self.canvas["height"]]

        self.create_visibles()
  
        self.canvas.tag_lower(self.id)
        self.canvas.tag_bind(self.id, "<B1-Motion>", self.move)
    

    def repaint(self):
        s = self.canvas._scale
        self.canvas.coords(self.id,
                           self.origo + self.value * s,
                           0,
                           self.origo + self.value * s,
                           self.canvas["height"])
                    
    def move(self, event):
        
        x = int(self.canvas.canvasx(event.x))
        s = self.canvas._scale
    
        if not self.value.names: 
           self.value.new_formula(str(x / s))
        
        self.canvas.repaint()
        

#-------------------------------------------------------------------------------

class _Y(VisualPrimitive):

    def __init__(self, canvas, value, origo):
        VisualPrimitive.__init__(self, canvas, value, origo)
        self.origo = origo
        
        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="gray")
        self.selected_fill = dict(fill="green")
        self.hidden_fill = dict(fill="")            
        
        self.list_param = [0, self.value, canvas["width"], self.value]
        self.kw_param = dict(width=1, fill="gray", tags=value.tag)
        
        self.create_visibles()
    
        self.canvas.tag_lower(self.id)
        self.canvas.tag_bind(self.tag, "<B1-Motion>", self.move)
    

    def repaint(self):
        s = self.canvas._scale
        self.canvas.coords(self.id,
                           0,
                           self.origo + self.value * s,
                           self.canvas["width"],
                           self.origo + self.value * s)
    def move(self, event):
        
        y = int(self.canvas.canvasx(event.y))
        s = self.canvas._scale
    
        if not self.value.names: 
           self.value.new_formula(str(y / s))
        
        self.canvas.repaint()
    
#-------------------------------------------------------------------------------    

class A(VisualPrimitive):
    
    def __init__(self, canvas, point, a, origo):
        VisualPrimitive.__init__(self, canvas, a, origo)
        self.origo = origo    
        self.point = point
        self.point.fellows.update({self.tag:self})

        self.active_fill = dict(fill="red")
        self.passive_fill = dict(fill="gray")
        self.selected_fill = dict(fill="green")
        self.hidden_fill = dict(fill="")
        
        self.list_param = [0,100,200,300]
        self.kw_param = dict(width=1, fill="gray", tags=self.tag)

        self.create_visibles()
        
        self.canvas.tag_lower(self.tag)
        self.canvas.tag_bind(self.tag, "<B1-Motion>", self.move)

    def move(self, event):

        x = int(self.canvas.canvasx(event.x))
        y = int(self.canvas.canvasy(event.y))

        xx = float(self.point.x)
        yy = float(self.point.y)

        a =  RadBetweenTwoPoint(x,y,xx,yy)
        
        if not self.value.names: 
           self.value.new_formula(str(a))
        
        self.canvas.repaint()
        
    def repaint(self):
        x = self.point.x
        y = self.point.y
        _x = self.origo + float(x) * self.canvas._scale
        _y = self.origo + float(y) * self.canvas._scale
        a = float(self.value)   

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

    def __init__(self, canvas, value, x, y):
        VisualPrimitive.__init__(self, canvas, value)
        self.x = x
        self.y = y

        self.active_fill = dict(fill="red", outline="black")
        self.passive_fill = dict(fill="", outline="gray")
        self.selected_fill = dict(fill="green", outline="black")
        self.hidden_fill = dict(fill="", outline="")            

        self.list_param = [x - 3, y - 3, x + 3, y + 3]
        self.kw_param = dict(fill="", outline="black", tags=value.tag)
        
        self.create_visibles()
        self.repaint()
        

    def repaint(self):
        x = self.canvas.coords(self.x.id)[0]
        y = self.canvas.coords(self.y.id)[1]
        self.canvas.coords(self.id, x - 3, y - 3, x + 3, y + 3)
