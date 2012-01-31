from Tkinter import *
from cad_kernel.db import Item


class VisualItem(Item):

    def __init__(self, canvas, base_tag, formula):
        Item.__init__(self, canvas.items, base_tag, str(formula))
        
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
        self.canvas.cmd.set(self.formula)
        self.canvas.e.bind("<KeyPress>", self.g)
        self.id_txt = self.canvas.create_window(x, y, window=self.canvas.e)
        
    def g(self, event):
        self.canvas.e['width'] = len(self.canvas.cmd.get()) + 1
        if event.keysym == "Return":
            self.new_formula(self.canvas.cmd.get())
            #self.canvas.items.recalc()
            self.canvas.repaint()
            self.canvas.delete(self.id_txt)
            self.canvas.focus_set()
            if self.tag[0] == "X" or self.tag[0] == "Y":
                self.hide()
        
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
        self.canvas.itemconfig(self.tag, self.passive_fill)

    def selected_color(self):
        self.canvas.itemconfig(self.tag, self.selected_fill)
        

    def hide(self, event=None):
        self.visible =  False
        self.unbind()
        self.canvas.itemconfig(self.tag, self.hidden_fill)
        
    def unhide(self):
        self.visible = True
        self.bindit()
        self.canvas.itemconfig(self.tag, self.passive_fill)

    def show(self):
        if not self.visible:
            self.canvas.tag_bind(self.tag, "<Enter>", self.mouse_enter)
            self.canvas.tag_bind(self.tag, "<Leave>", self.mouse_leave)
            self.canvas.tag_bind(self.tag, "<Button-1>", self.mouse_select)
            self.canvas.itemconfig(self.tag, self.passive_fill)

    def unshow(self):
        if not self.visible:
            self.hide()
        else:
            self.unhide()
            
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
        print self.tag, "=", self.value

        
