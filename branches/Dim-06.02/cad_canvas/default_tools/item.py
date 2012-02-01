from Tkinter import *
from cad_kernel import *

class Item(item.Item):

    def __init__(self, canvas, base_tag, formula):
        item.Item.__init__(self, canvas.items, base_tag, formula)
        self.canvas = canvas

        self.active_fill = None
        self.passive_fill = None
        self.selected_fill = None

        self.org_point = None
        self.id = None
        self.selected = False

           
                           
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
        self.canvas.cmd.set(self.formula)
        self.canvas.e.bind("<KeyPress>", self.g)
        self.id_txt = self.canvas.create_window(event.x, event.y,
                                                window=self.canvas.e)

    def g(self, event):
        self.canvas.e['width'] = len(self.canvas.cmd.get()) + 1
        if event.keysym == "Return":
            self.new_formula(self.canvas.cmd.get())
            self.canvas.repaint()
            self.canvas.delete(self.id_txt)
        
    def mouse_select(self, event):

        if self.selected:
            self.active_color()
            self.selected = False
        else:
            self.selected_color()
            self.selected = True
            
            
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

    def delete(self):
        self.canvas.delete(self.tag)
        self.canvas.items.pop(self.tag)
                
    def addtag(self, tag):
        self.canvas.addtag_withtag(tag, self.tag)

    def canvasx(self, x):
        return self.canvas.canvasx(x)          

    def canvasy(self, y):
        return self.canvas.canvasy(y)          

    def __getstate__(self):    
        odict = self.__dict__.copy() # copy the dict since we change it    
        
        odict['canvas'] = None
        odict['e'] = None
        odict['id_txt'] = None
        odict['code'] = None
        odict['db'] = None
        
        for t in odict:
            print t,"=",odict[t]

        return odict

    
    def __setstate__(self, dicti):
        self.__dict__.update(dicti)   # update attributes
        
    
    def print_status(self, event=None):
        print self.tag

        for kw in self.fellows:
            print "\t\t",
            print kw + "->",
            for fell in self.fellows[kw].fellows:
                print fell,
            print

