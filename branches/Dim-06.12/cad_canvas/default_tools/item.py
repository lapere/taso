from Tkinter import *
from cad_kernel.db import Item, x_element, y_element, angle_element


class VisualBaseItem:

    def __init__(self, canvas):

        self.tag = self.value.tag
        self.value.repaint = self.repaint
        self.value.visual = self
        
        self.canvas = canvas

        self.active_fill = None
        self.passive_fill = None
        self.selected_fill = None
        self.hidden_fill = None

        self.org_point = None
        self.id = None
        self.selected = False
        self.visible = True
        self.showed = False
        self.fellows = dict()
           
                           
    def bindit(self):
        self.canvas.tag_bind(self.tag, "<Button-1>", self.mouse_push)
        self.canvas.tag_bind(self.tag, "<Shift-Button-1>", self.mouse_select)
        self.canvas.tag_bind(self.tag, "<Enter>", self.mouse_enter)
        self.canvas.tag_bind(self.tag, "<Leave>", self.mouse_leave)
        self.canvas.tag_bind(self.tag, "<Double-Button-1>", self.mouse_double)
        self.canvas.tag_bind(self.tag, "<Double-Button-3>", self.print_status)

    
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
            self.canvas.items.recalc()
            self.canvas.repaint()
            self.canvas.delete(self.id_txt)
            self.canvas.focus_set()
        
    def mouse_select(self, event):

        if self.visible:
            self.hide()
        else:
            self.unhide()
            
            
    def repaint(self):
        pass
        
    def active_color(self):
        self.canvas.itemconfig(self.tag, self.active_fill)

    def passive_color(self):
        if self.selected:
            self.canvas.itemconfig(self.tag, self.selected_fill)
        else:
            self.canvas.itemconfig(self.tag, self.passive_fill)

    def selected_color(self):
        self.canvas.itemconfig(self.tag, self.selected_fill)
        

    def hide(self, event=None):
        self.visible =  False
        self.canvas.tag_unbind(self.tag, "<Leave>")
        self.canvas.tag_unbind(self.tag, "<Enter>")
        self.canvas.itemconfig(self.tag, self.hidden_fill)
        
    def unhide(self):
        self.visible = True
        self.canvas.tag_bind(self.tag, "<Leave>", self.mouse_leave)
        self.canvas.tag_bind(self.tag, "<Enter>", self.mouse_enter)
        self.canvas.itemconfig(self.tag, self.passive_fill)

    def show(self):
        self.showed = True
        self.canvas.itemconfig(self.tag, self.passive_fill)
        self.canvas.tag_bind(self.tag, "<Leave>", self.mouse_leave)
        self.canvas.tag_bind(self.tag, "<Enter>", self.mouse_enter)

    def unshow(self):
        self.showed = False
        if self.visible:
            self.unhide()
        else:
            self.hide()
        
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
            return float(self.value)
        except:
            return None
    
    def __getstate__(self):    
        odict = self.__dict__.copy() # copy the dict since we change it    
        odict['canvas'] = None
        
        for t in odict:
            print t,"=",odict[t]

        
        #odict['value'].repaint = None
        #odict['value'].visual = None
        
        return odict

    
    def __setstate__(self, dicti):
        if dicti:
            self.__dict__.update(dicti)   # update attributes
        
    
    def print_status(self, event=None):
        print self.tag, self.value.names

        

class VisualItem(VisualBaseItem):
    def __init__(self, canvas, base_tag, formula=None):
        self.value = Item(canvas.items, base_tag, str(formula))
        VisualBaseItem.__init__(self, canvas)

class VisualXItem(VisualBaseItem):
    def __init__(self, canvas, base_tag, formula=None):
        self.value = x_element(canvas.items, base_tag, str(formula))
        VisualBaseItem.__init__(self, canvas)

class VisualYItem(VisualBaseItem):
    def __init__(self, canvas, base_tag, formula=None):
        self.value = y_element(canvas.items, base_tag, str(formula))
        VisualBaseItem.__init__(self, canvas)

class VisualAngleItem(VisualBaseItem):
    def __init__(self, canvas, base_tag, x, y, formula=None):
        self.value = angle_element(canvas.items, base_tag, x, y, str(formula))
        VisualBaseItem.__init__(self, canvas)
