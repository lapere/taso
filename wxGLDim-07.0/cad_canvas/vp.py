from cad_kernel.db import Item
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import copy
        

class VisualBase(Item):
    cnt = 0
    def __init__(self, canvas, db, base_tag, formula):
        Item.__init__(self, db, base_tag, str(formula))
        VisualBase.cnt += 1
        self.id = VisualBase.cnt
        canvas.visuals.update({self.id:self})
        self.value = formula
        self.canvas = canvas

        self.active_fill = [1.0, 0.0, 0.0]
        self.passive_fill = [0.2, 0.2, 0.2]
        self.selected_fill = [0.0, 1.0, 0.0]
        
        self.selected = False
        self.visible = True
        self.passive_color()
        self.create_visibles()
        
    def create_visibles(self):
        pass
                           
    def bindit(self):
        self.mouse_push = True
        self.mouse_select = True
        self.mouse_enter = True
        self.mouse_leave = True
        self.mouse_double = True
        self.print_status = True

    def unbind(self):
        self.mouse_push = False
        self.mouse_select = False
        self.mouse_enter = False
        self.mouse_leave = False
        self.mouse_double = False
        self.print_status = False

    def mouse_enter(self, event):
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
        self.color = self.active_fill

    def passive_color(self):
        self.color = self.passive_fill

    def selected_color(self):
        self.color = self.value.selected_fill
        
    def hide(self, event=None):
        self.unbind()
        self.color = self.hidden_fill
        
    def unhide(self):
        self.bindit()
        self.color = self.passive_fill
        
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

class VerticalLine(VisualBase):

    def __init__(self, canvas, value, offset):
        VisualBase.__init__(self, canvas, value, offset)
        
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

class HorizontalLine(VisualBase):

    def __init__(self, canvas, value, offset):
        VisualBase.__init__(self, canvas, value, offset)
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

class AngledLine(VisualBase):
    
    def __init__(self, canvas, x, y, a, offset):
        VisualBase.__init__(self, canvas, (x,y,a), offset)

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

class Point(VisualBase):

    def create_visibles(self):
        self.bindit()
        self.repaint()
        
    def repaint(self, mode=None):
        if mode == GL_SELECT:
            glLoadName(self.id)
        x, y = self.value
        glColor3f(*self.color)
        glBegin(GL_POINTS)
        glVertex2fv((float(x), float(y)))
        glEnd()
 

#-------------------------------------------------------------------------------

class Line(VisualBase):
    
    def repaint(self, mode=None):
        if mode == GL_SELECT:
            glLoadName(self.id)
        x0,y0,x1,y1 = self.value
        glColor3f(*self.color)
        glBegin(GL_LINES)
        glVertex2fv((float(x0), float(y0)))
        glVertex2fv((float(x1), float(y1)))
        glEnd()
        
