from Tkinter import *
from time import sleep
from default_tools import *
from cad_kernel import db
import tkFileDialog
from math import *
import pickle
from scroll import *

class cad_canvas(ScrolledCanvas):

    current = None
    
    def __init__(self, master, ic, **kw):
        ScrolledCanvas.__init__(self, master, **kw)
        self.sema = False
        self.x = None
        self.y = None
        self.mx = None
        self.my = None
        self._more = True   
        self.dim = None
        self.tmp = None
        self.items = db.ItemDB(ic)
        self.visuals = dict()
        self.id = None
        self.panx = 0
        self.panx = 0
        self.lastx = 0
        self.lasty = 0
        self._scale = 1.0
        
        self.cmd = StringVar(self)
        self.e = Entry(self, width=3, bg="white",
                       relief=FLAT, bd=0, textvariable=self.cmd)
        
        #self.bind("<Button-3>", self.noMore)
        #self.bind_all("<KeyPress-Shift_L>", self.shift_press) 
        #self.bind_all("<KeyRelease-Shift_L>", self.shift_release)
        self.origo = 0.0
        self.current_item = None
        
    def shift_press(self, event):
        for tag in self.items:
            self.items[tag].unhide()

    def shift_release(self, event):
        for tag in self.items:
            if not self.items[tag].visible:
                self.items[tag].hide()   
        
    def noMore(self, event):
        self.delete(self.id)
        self.bind("<Button-3>", self.noMore)
        self.unbind("<Button-1>")
        self.unbind("<Motion>")
        self['cursor'] = "top_left_arrow"
        self._more = False
        
        
    def get_point(self, event=None):
        if not event:
            self.bind("<Button-1>", self.get_point)
            self.sema = True
            self._more = True

            while self.sema:
                self.update()
                sleep(0.1)
                if not self._more:
                    return None
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

    
    def xItem(self):
        
        while self._more:
            self.xElement()
            
    def X(self, value):
        return vp.X(self, value, self.origo)

    def Y(self, value):
        return vp.Y(self, value, self.origo)

    def Point(self, x, y):
        return vp.Point(self, x, y)
        
    def xElement(self, value=None):
        tmp = None
        if value != None:
            tmp =  vp.X(self, value, self.origo)
        else:
            x, y = self.get_point()
            hit = self.find_olap("X")
            if hit:
                return hit
            elif x:
                tmp = vp.X(self, x, self.origo)

        tmp.repaint()
        if self._more:
            self.xElement()
        else:
            return tmp
           


            
    def yElement(self, value=None):
        tmp = None
        if value != None:
            tmp = Yelement(self, value)
        else:
            x, y = self._get_point()
            hit = self.find_olap("Y")
            if hit:
                return hit
            elif y:
                tmp =  Yelement(self, y)

        #self.items.recalc()
        tmp.repaint()
        return tmp       
             
    def zElement(self, value=None):
        tmp = None
        if value != None:
            tmp = Zelement(self, value)
        else:
            x, y = self._get_point()
            hit = self.find_olap("Z")
            if hit:
                return hit
            elif y:
                tmp =  Zelement(self, y)

        #self.items.recalc()
        tmp.repaint()
        return tmp   

    def point(self, x=None, y=None, z = None):
        self._get_point()
        hits = self.find_olap()
        m = map(lambda x: x[0], hits)

        pcnt = m.count("P")
        xcnt = m.count("X")
        ycnt = m.count("Y")
        zcnt = m.count("Z")

        if pcnt:
             return self.find_olap("P")
        else:
            if x == None:
                x = self.xElement()
            if y == None:
                y = self.yElement()
            if z == None:
                z = self.zElement()

            p = Point(self, x, y, z)
            p.repaint()
            return p

    def angleElement(self, point=None, value=None):
        if point != None and value != None:
            tmp = _A(self, point, value)
        else:
            Xelement,Yelement  = self._get_point()
            
            hits = self.find_olap()
            m = map(lambda x: x[0], hits)
            
            acnt = m.count("A")
            xcnt = m.count("X")
            ycnt = m.count("Y")
                
            if xcnt:
                x = self.find_olap("X")
            else:
                x = self.xElement(Xelement)

            if ycnt:
                y = self.find_olap("Y")
            else:
                y = self.yElement(Yelement)

            point = self.point(x,y)

            if value == None:
                x1 = point.x
                y1 = point.y
                x2, y2 = self._get_point()
                value = RadBetweenTwoPoint(x1, y1, x2, y2)
                
            tmp = _A(self, point, value)

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

    def xspace(self, x0=None, x1=None):
        if x0 == None:
            x0 = self.xElement()
        if x1 == None:
            x1 = self.xElement()
        t = XSpace(self, x0, x1) 
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
                    self.items[tag].visible = False
                    self.items[tag].hide()

    def unhide(self, event=None):
        if not event:
            self.bind("<Button-1>", self.unhide)
        else:
            tag = self.get_current()
            if tag:
                if self.items.has_key(tag):
                    self.items[tag].visible = True
                    self.items[tag].unhide()
                    
    def repaint(self):
        for i in self.visuals:
            self.visuals[i].repaint()
                
    def _print(self):
        fn = tkFileDialog.asksaveasfilename(filetypes=[('Postscript files', '*.ps')])
        self.focus_set()
        self.update_idletasks()
        self.postscript(colormode="gray", file=fn)


    def open_db(self):
        fn = tkFileDialog.askopenfilename(filetypes=[('db files', '*.db'),('All files', '*.*')])
        self.items.update(pickle.load(open(fn)))
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
