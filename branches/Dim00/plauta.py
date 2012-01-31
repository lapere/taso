from Tkinter import *
from dimension import *
from element import *
from fellow import *
from level import _X, _Y
from line import *
from point import *
from time import sleep
import tkFileDialog
import pickle
import shelve

class PLauta(Canvas):

    current = None
    
    def __init__(self, master, **kw):
        Canvas.__init__(self, master, kw)
        self.sema = False
        self.x = None
        self.y = None
        self.mx = None
        self.my = None
        self.xgap = 0
        self.ygap = 0
        self._more = True   
        self.dim = None
        self.tmp = None
        self.items = dict()
        self.id = None
        self.panx = 0
        self.panx = 0
        self.lastx = 0
        self.lasty = 0
        self._scale = 1.0
    
        
        self.bind("<Button-3>", self.noMore)
        self.bind("<Double-Button-1>", self.print_status)

    def _move(self, event):
        self.mx = event.x
        self.my = event.y
        
    def noMore(self, event):
        self.delete(self.id)
        self.bind("<Button-3>", self.noMore)
        self.unbind("<Button-1>")
        self.unbind("<Motion>")
        self['cursor'] = "top_left_arrow"
        self._more = False
        
        
    def _get_point(self, event=None):
        self.x = _X(event.x + self.xgap)
        self.y = _Y(event.y + self.ygap)
        self.unbind("<Button-1>")
        self.sema = False
    
    def getPoint(self, event=None, rubber=None):
        self.bind("<Button-1>", self._get_point)
        
        if rubber:
            self.bind("<Motion>", self._move)

        self.sema = True
        self._more = True
        
        while self.sema:

            if rubber and self.mx:
                self.id = self.create_line(rubber.x.x, rubber.y.y,
                                        self.mx, self.my)
                self.tag_lower(self.id)

            self.update()
            sleep(0.1)

            if rubber:
                self.delete(self.id)

            self.update()

            if not self._more:
                return None
        
        tags = self.gettags(CURRENT)
        cur = self.type(CURRENT)

        for t in tags:
            if t != "current":
                tag = t
                
        if cur == "rectangle":
            return self.items[tag]
                    
        elif cur == "line":
            endp = self.point(self.x, self.y)
            startp0, startp1 = self.items[tag].get_ends()
            style = self.items[tag].style
            self.delete(tag)
            self.items.pop(tag)

            startp0.fellows.pop(tag)
            startp1.fellows.pop(tag)
            
            Line(self, startp0, endp, style=style)
            Line(self, startp1, endp, style=style)
            
            return endp
        else:
            p = self.point(self.x, self.y)
            return p
        

    def line(self, startp=None, endp=None):
        if startp == None:
            startp = self.getPoint()
        if endp == None:
            endp = self.getPoint(rubber=startp)
            self._more = True
        else:
            self._more = False

        if startp and endp:    
            l = Line(self, startp, endp)
            self.items[l.tag] = l
        else:
            return

        if self._more:
            self.line(startp=endp)

        return l

    def point(self, x, y):
        p = Point(self, x,  y)
        self.items[p.tag] = p
        return p

    def get_e(self, event, tags=None):

        if not tags:
            tags = self.gettags(CURRENT)

        pnts = []

        print "Element" + "-" * (80-len("Element"))

        for t in tags:

            if t[0] == 'P':
                pnts.append(self.items[t])
                
            elif t[0] == 'L':
                startp0, startp1 = self.items[t].get_ends()
                pnts.append(startp0)
                pnts.append(startp1)

        for point in pnts:
            for fell in point.fellows:
                if fell[0] == 'E':
                    element = point.fellows[fell]
                    if self.tmp.typ == element.typ:
                        for pal in element.fellows:
                            p = element.fellows[pal]
                            self.tmp.new_fellow(p)
                            p.fellows.pop(fell)
                            p.new_fellow(self.tmp)
                        if fell != self.tmp.tag:
                            self.items.pop(fell)
                                
            self.tmp.new_fellow(point)

        if self.tmp.typ == "x":
            self.xelement()
        else:
            self.yelement()

        self.repaint()
        print "-" * 80

    def clean(self, tag):

        item = []

        for i in self.items:
            for fell in self.items[i].fellows:
                if fell == tag:
                    item.append(self.items[i])

        for i in item:    
            i.fellows.pop(tag)

    def element(self, typ, items):
        e  = Element(self, typ)
        self.items[e.tag] = e
        for item in items:
            e.new_fellow(item)
        return e
        
    def xelement(self):
        e  = Element(self, "x")
        self.items[e.tag] = e
        self['cursor'] = "sb_v_double_arrow"
        self.bind("<Button-1>", self.get_e)
        self._more = True
        self.tmp = e

    def yelement(self):
        e  = Element(self, "y")
        self.items[e.tag] = e
        self['cursor'] = "sb_h_double_arrow"
        self.bind("<Button-1>", self.get_e)
        self._more = True
        self.tmp = e

    def xdimension(self):
        self.typ_dimension("x")

    def ydimension(self):
        self.typ_dimension("y")
        
    def typ_dimension(self, typ):

        e0 = None
        e1 = None
        
        p0 = self.getPoint()
        p1 = self.getPoint()

        for fell in p0.fellows:
            if fell[0] == 'E':
                if p0.fellows[fell].typ == typ:
                    e0 = p0.fellows[fell]

        for fell in p1.fellows:
            if fell[0] == 'E':
                if p1.fellows[fell].typ == typ:
                    e1 = p1.fellows[fell]

        if not e0:
            e0 = self.element(typ, [p0])
        if not e1:
            e1 = self.element(typ, [p1])
            
        e = (e0, e1) 

        d = Dimension(self, e, typ)
        self.items[d.tag] = d

    def _del(self, event=None):        
        tags = self.gettags(CURRENT)
        
        for t in tags:
            if t[0] == 'L':
                self.items[t].delete()
                self.items.pop(t)
            if t[0] == 'P':
                self.items[t].delete()
                self.items.pop(t)
                
    def _delete(self, event=None):
        self.bind("<Button-1>", self._del)
    
    def repaint(self):
        for tag in self.items:
            if tag[0] != 'E':
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
        print "Items"
        for kw in self.items:
            print "\t",
            self.items[kw].print_status()
        if event:
            print "canvas h=", self["height"]
