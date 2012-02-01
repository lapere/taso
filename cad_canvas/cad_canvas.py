from Tkinter import *
from time import sleep
from default_tools.level import _X,_Y,_A
from default_tools.point import Point
from default_tools.line import Line
from default_tools.text import Txt
from default_tools.utils import *

from cad_kernel import db
import tkFileDialog
from math import *
import pickle
from scroll import *

class cad_canvas(ScrolledCanvas):

    current = None
    
    def __init__(self, master, **kw):
        ScrolledCanvas.__init__(self, **kw)
        self.sema = False
        self.x = None
        self.y = None
        self.mx = None
        self.my = None
        self._more = True   
        self.dim = None
        self.tmp = None
        self.items = db.ItemDB(None)
        self.id = None
        self.panx = 0
        self.panx = 0
        self.lastx = 0
        self.lasty = 0
        self._scale = 1.0
        self.master = master

        self.cmd = StringVar(self)
        self.e = Entry(self, width=3, bg="white",
                       relief=FLAT, bd=0, textvariable=self.cmd)
        
        self.bind("<Button-3>", self.noMore)
        self.bind_all("<KeyPress-a>", self.shift_press) 
        self.bind_all("<KeyRelease-a>", self.shift_release) 

    def shift_press(self, event):
        self.unbind("<Button-1>")
        for tag in self.items:
            self.items[tag].show()

    def shift_release(self, event):
        for tag in self.items:
            self.items[tag].unshow()   
        
    def noMore(self, event):
        self.delete(self.id)
        self.bind("<Button-3>", self.noMore)
        self.unbind("<Button-1>")
        self.unbind("<Motion>")
        self['cursor'] = "top_left_arrow"
        self._more = False
        
        
    def _get_point(self, event=None):
        if not event:
            self.bind("<Button-1>", self._get_point)
            self.sema = True
            self._more = True

            while self.sema:
                self.update()
                sleep(0.1)
                if not self._more:
                    return None, None
            return self.x / self._scale, self.y / self._scale
        else:
            self.x = self.canvasx(event.x) 
            self.y = self.canvasy(event.y) 
            self.sema = False
            
    
    
    def find_olap(self, typ=None,):
        t = self.find_overlapping(self.x - 5,
                                      self.y - 5,
                                      self.x + 5,
                                      self.y + 5)
        
        _list = []

        for tag in t:
            for tagg in self.gettags(tag):
                if tagg != "current":
                    v = self.items[tagg] 
                    if v.visible or v.showed:
                        _list.append(tagg)
                    if tagg[0] == typ:
                        if v.visible or v.showed:
                            return self.items[tagg]
        
        return _list
                
    def get_current(self):
        tags = self.gettags(CURRENT)
        tag = None
        for t in tags:
            if t != "current":
                tag = t
        return tag

    

    def xElement(self, value=None):
        tmp = None
        if value != None:
            tmp =  _X(self, value)
        else:
            x, y = self._get_point()
            hit = self.find_olap("X")
            if hit:
                return hit
            elif x:
                tmp = _X(self, x)

        #self.items.recalc()
        #tmp.calc()
        tmp.repaint()
        return tmp
           
            
    def yElement(self, value=None):
        tmp = None
        if value != None:
            tmp = _Y(self, value)
        else:
            x, y = self._get_point()
            hit = self.find_olap("Y")
            if hit:
                return hit
            elif y:
                tmp =  _Y(self, y)

        #self.items.recalc()
        tmp.repaint()
        return tmp

        
    
    def point(self, x=None, y=None):

        if x != None and y != None:
            p = Point(self, x, y)
            self.items.recalc()
            self.repaint()
            return p
        
        _x, _y = self._get_point()
        
        if x == None and y == None:
            
            hits = self.find_olap()
            m = map(lambda x: x[0], hits)

            #if m.count("P"):
            #    return self.find_olap("P")
            
            acnt = m.count("A")
            xcnt = m.count("X")
            ycnt = m.count("Y")
            
            if ycnt:
                y = self.find_olap("Y")
                    
            if xcnt:
                x = self.find_olap("X")

            if x and y:
                l = list(set(x.fellows.keys()) & set(y.fellows.keys()))
                for i in l:
                    if i[0] == "P":
                        return self.items[i]
                    
            if x and acnt and not y:
                a = self.find_olap("A")
                y = self.yElement(100)
                y.new_formula("solvey(%s,%s)" % (a.tag, x.tag))

            if y and acnt and not x:
                a = self.find_olap("A")
                x = self.xElement(100)
                x.new_formula("solvex(%s,%s)" % (a.tag, y.tag))

            if acnt == 1 and not x and not y:
                a = self.find_olap("A")
                val = a()
                if cos(val) > sin(val):
                    x = self.xElement(_x)
                    y = self.yElement(100)
                    y.new_formula("solvey(%s,%s)" % (a.tag, x.tag))
                else:
                    y = self.yElement(_y)
                    x = self.xElement(100)
                    x.new_formula("solvex(%s,%s)" % (a.tag, y.tag))
                    
            elif acnt == 2 and not x and not y:
                a = filter(lambda x: x[0] == "A", hits)
                x = self.xElement(_x)
                y = self.yElement(_y)
                x.new_formula("solvex(%s,%s)" % (a[0], a[1]))
                y.new_formula("solvey(%s,%s)" % (a[0], a[1]))
                    
        if x == None:
            x = self.xElement(_x)
            #x.calc()
        if y == None:
            y = self.yElement(_y)
            #y.calc()

        p = Point(self, x, y)
        #self.items.recalc()
        p.repaint()
        return p

    def angleElement(self, point=None, value=None):
        if point != None and value != None:
            tmp = _A(self, point, value)
        else:
            _x,_y  = self._get_point()
            
            hits = self.find_olap()
            m = map(lambda x: x[0], hits)

            if m.count("A") and not m.count("P"):
                return self.find_olap("A")
            
            pcnt = m.count("P")
            xcnt = m.count("X")
            ycnt = m.count("Y")

            
            if pcnt:
                point = self.find_olap("P")
            else:
                if xcnt:
                    x = self.find_olap("X")
                else:
                    x = self.xElement(_x)

                if ycnt:
                    y = self.find_olap("Y")
                else:
                    y = self.yElement(_y)

                point = self.point(x,y)

            if value == None:
                x1 = point.x
                y1 = point.y
                x2, y2 = self._get_point()
                value = RadBetweenTwoPoint(x1, y1, x2, y2)
                
            tmp = _A(self, point, value)

        #self.items.recalc()
        tmp.repaint()
        return tmp

    def line(self, startp=None, endp=None):
        if startp == None:
            startp = self.point()
        if endp == None:
            endp = self.point()
        li = Line(self, startp, endp)
        li.pen(2)
        #self.items.recalc()
        li.repaint()
        if self._more:
            self.line(startp=endp)
        return li

    def text(self, point=None, text=None):
        if point == None:
            point = self.point()
        t = Txt(self, point, text)
        #self.items.recalc()
        t.repaint()
        return t
    
                 
    def _delete(self, event=None):
        if not event:
            self.bind("<Button-1>", self._delete)
        else:
            tag = self.get_current()
            if tag:
                if self.items.has_key(tag):
                    self.items[tag].delete()

    def hide(self, event=None):
        if not event:
            self.bind("<Button-1>", self.hide)
        else:
            tag = self.get_current()
            if tag:
                if self.items.has_key(tag):
                    self.items[tag].hide()

    def unhide(self, event=None):
        if not event:
            self.bind("<Button-1>", self.unhide)
        else:
            tag = self.get_current()
            if tag:
                if self.items.has_key(tag):
                    self.items[tag].unhide()
                    
    def repaint(self):
        #for i in "X", "Y", "P", "A", "L", "T":
            for tag in self.items:
         #       if tag[0] == i:
                    self.items[tag].repaint()
                
    def _print(self):
        fn = tkFileDialog.asksaveasfilename(filetypes=[('Postscript files', '*.ps')])
        self.focus_set()
        self.update_idletasks()
        self.postscript(colormode="gray", file=fn)


    def open_db(self):
        fn = tkFileDialog.askopenfilename(filetypes=[('db files', '*.db'),('All files', '*.*')])
        self.items.update(pickle.load(open(fn)))
        self.items.recalc()
        for i in self.items:
            self.items[i].canvas = self
            self.items[i].create_visibles()
            
        self.repaint()

    def _save(self):
        fn = tkFileDialog.asksaveasfilename(filetypes=[('PRCad files', '*.pr')])
        fd = open(fn,'w+')
        pickle.dump(self.items, fd)
        fd.close()

    def _open(self):
        fn = tkFileDialog.askopenfilename(filetypes=[('PRCad files', '*.pr'),('All files', '*.*')])
        self.items = pickle.load(open(fn))
        self.items.ic = self.ic
        
        for i in self.items:
            self.items.ic.locals[i] = self.items[i]
            self.items[i].canvas = self
            self.items[i].create_visibles()
        
        self.repaint()

    def _new(self):
        self.delete("all")
        self.items = db.ItemDB(self.ic)
        self.repaint()
        
    def print_status(self, event=None):
        for kw in self.items:
            print "\t",
            print kw,
            if self.items[kw]():
                print self.items[kw]()    
