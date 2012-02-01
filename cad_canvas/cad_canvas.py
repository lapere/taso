from Tkinter import *
from time import sleep
from default_tools.level import _X,_Y,_A
from default_tools.point import Point
from default_tools.line import Line
from default_tools.utils import *

from cad_kernel import db
import tkFileDialog
from math import *
import pickle

class cad_canvas(Canvas):

    current = None
    
    def __init__(self, master, **kw):
        Canvas.__init__(self, master, kw)
        self.sema = False
        self.x = None
        self.y = None
        self.mx = None
        self.my = None
        self._more = True   
        self.dim = None
        self.tmp = None
        self.items = db.ItemDB()
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
            return self.x, self.y
        else:
            self.x = self.canvasx(event.x)
            self.y = self.canvasy(event.y)
            self.sema = False
            
    
    
    def find_olap(self, typ):
        t = self.find_overlapping(self.x - 10,
                                      self.y - 10,
                                      self.x + 10,
                                      self.y + 10)
        for tag in t:
            for tagg in self.gettags(tag):
                if tagg[0] == typ:
                    return self.items[tagg].visual
        return None
                
    def get_current(self):
        tags = self.gettags(CURRENT)
        tag = None
        for t in tags:
            if t != "current":
                tag = t
        return tag

    

    def xElement(self, value=None):
        if value:
            return _X(self, value)
        else:
            x, y = self._get_point()
            hit = self.find_olap("X")
            if hit:
                return hit
            elif x:
                return _X(self, x)
           
            
    def yElement(self, value=None):
        if value:
            return _Y(self, value)
        else:
            x, y = self._get_point()
            hit = self.find_olap("Y")
            if hit:
                return hit
            elif y:
                return _Y(self, y)

        
    
    def point(self, x=None, y=None):

        _x, _y = self._get_point()

        if not x and not y:

            hit = self.find_olap("P")
            if hit:
                return hit

            hit = self.find_olap("X")
            if hit:
                x = hit

            hit = self.find_olap("Y")
            if hit:
                y = hit

        if not x:
            x = self.xElement(_x)
            x.value.calc()
        if not y:
            y = self.yElement(_y)
            y.value.calc()

        return Point(self, x, y)

    def angleElement(self, point=None, value=None):
        if not point:
            point = self.point()
        if not value:
            x2, y2 = self._get_point()
            value = RadBetweenTwoPoint(point.x(), point.y(), x2, y2)
            
        a = _A(self, point.x.value, point.y.value, value)
        self.items.recalc()
        self.repaint()
        return a

    def line(self, startp=None, endp=None):
        if not startp:
            startp = self.point()
        if not endp:
            endp = self.point()
        return Line(self, startp, endp)
    
                 
    def _delete(self, event=None):
        if not event:
            self.bind("<Button-1>", self._delete)
        else:
            tag = self.get_current()
            if tag:
                if self.items.has_key(tag):
                    self.delete(tag)
                    self.items.pop(tag)
                
    
    def repaint(self):
        for tag in self.items:
                self.items[tag].repaint()

    def _print(self):
        fn = tkFileDialog.asksaveasfilename(filetypes=[('Postscript files', '*.ps')])
        self.focus_set()
        self.update_idletasks()
        self.postscript(colormode="gray", file=fn)

    def _save(self):
        fn = tkFileDialog.asksaveasfilename(filetypes=[('PRCad files', '*.pr')])
        fd = open(fn,'w+')
        pickle.dump(self.items, fd)
        fd.close()

    def _open(self):
        fn = tkFileDialog.askopenfilename(filetypes=[('PRCad files', '*.pr'),('All files', '*.*')])
        self.items.update(pickle.load(open(fn)))
        
        for i in self.items:
            self.items[i].canvas = self

        for item in 'P', 'L' ,'E', 'D':
            for i in self.items:
                if i[0] == item:
                    if not self.find_withtag(i):
                        self.items[i].create_visibles()
            
        self.repaint()
          
    def print_status(self, event=None):
        for kw in self.items:
            print "\t",
            print kw,
            if self.items[kw]():
                print self.items[kw]()    
