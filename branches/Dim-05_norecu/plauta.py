from Tkinter import *
from dimension import *
from element import *
from fellow import *
from level import _X, _Y
from line import *
from arc import *
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
        self.master = master
        
        self.bind("<Button-3>", self.noMore)
        
        
    def _move(self, event):
        self.mx = self.canvasx(event.x)
        self.my = self.canvasy(event.y)
        
    def noMore(self, event):
        self.delete(self.id)
        self.bind("<Button-3>", self.noMore)
        #self.unbind("<Button-1>")
        self.unbind("<Motion>")
        self['cursor'] = "top_left_arrow"
        self._more = False
        
        
    def _get_point(self, event=None):
        self.x = self.canvasx(event.x)
        self.y = self.canvasy(event.y)
        #self.unbind("<Button-1>")
        self.sema = False
    
    def getPoint(self, event=None, rubber=None):
        self.bind("<Button-1>", self._get_point)
        
        if rubber:
            self.bind("<Motion>", self._move)

        self.sema = True
        self._more = True
        
        while self.sema:

            if rubber and self.mx:
                self.id = self.create_line(rubber.x(), rubber.y(),
                                        self.mx, self.my)
                self.tag_lower(self.id)

            self.update()
            sleep(0.1)

            if rubber:
                self.delete(self.id)

            self.update()

            if not self._more:
                return None
        
        tag = self.get_current()

        if tag[0] == "P":
            if rubber != self.items[tag]:
                return self.items[tag]
                    
        elif tag[0] == "L":
            line = self.items[tag]
            startp0, startp1 = line.get_ends()
            
            if line.typ() == "x":
                y = self.find_olap("Y")
                if not y:
                    y = _Y(self, self.y)
                x = startp0.x
            elif line.typ() == "y":
                x = self.find_olap("X")
                if not x:
                    x = _X(self, self.x)
                y = startp0.y
            else:
                x = _X(self, self.x)
                y = _Y(self, self.y)
                
            
            endp = self.point(x, y)
            
            style = self.items[tag].style
            self.delete(tag)
            self.items.pop(tag)

            startp0.fellows.pop(tag)
            startp1.fellows.pop(tag)
            
            Line(self, startp0, endp, style=style)
            Line(self, startp1, endp, style=style)
            
            return endp

        elif tag[0] == "X":
            y = self.find_olap("Y")
            if not y:
                y = _Y(self, self.y)
            p = self.point(self.items[tag], y)
            return p
        elif tag[0] == "Y":
            x = self.find_olap("X")
            if not x:
                x = _X(self, self.x)
            p = self.point(x, self.items[tag])
            return p
        else:
            x = _X(self, self.x)
            y = _Y(self, self.y)
            p = self.point(x, y)
            return p

    def find_olap(self, typ):
        t = self.find_overlapping(self.x - 5,
                                      self.y - 5,
                                      self.x + 5,
                                      self.y + 5)
        for tag in t:
            for tagg in self.gettags(tag):
                if tagg[0] == typ:
                    return self.items[tagg]
        return None
                
    def get_current(self):
        tags = self.gettags(CURRENT)
        tag = [None]
        for t in tags:
            if t != "current":
                tag = t
        return tag

    def arc_3p(self):
        startp = self.getPoint()
        midp = self.getPoint()
        endp = self.getPoint()
        c = Arc(self, startp=startp, midp=midp, endp=endp)
        self.items[c.tag] = c
        self.line(startp=endp)
        
    def arc_sce(self):
        startp = self.getPoint()
        center = self.getPoint()
        endp = self.getPoint()
        c = Arc(self, startp=startp, center=center, endp=endp)
        self.items[c.tag] = c
        self.line(startp=endp)

    def arc_sca(self):
        pass
    def arc_scl(self):
        pass
    def arc_sea(self):
        pass
    def arc_sed(self):
        pass
    def arc_ser(self):
        pass
    def arc_cse(self):
        pass
    def arc_csa(self):
        pass
    def arc_csl(self):
        pass

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

    def get_e(self, event):
        curr = self.get_current()    

        if curr[0] == "X" or curr[0] == "Y":
            self.tmp.append(curr)
        else:
            return
        
        if len(self.tmp) == 2:
            if self.tmp[0][0] == self.tmp[1][0]:
                self.tmp.append(curr)
                e = (self.items[self.tmp[0]], self.items[self.tmp[1]]) 
                d = Dimension(self, e, curr[0])
                self.items[d.tag] = d
                self.unbind("<Button-1>")
        else:
            self.tmp = [curr]


    def join_elements(self, element, to):

        if to.typ == element.typ:
            for pal in element.fellows:
                p = element.fellows[pal]
                to.new_fellow(p)
                p.fellows.pop(element.tag)
                p.new_fellow(to)
            if element.tag != to.tag:
                self.items.pop(element.tag)

    def clean(self, tag):

        item = []

        for i in self.items:
            for fell in self.items[i].fellows:
                if fell == tag:
                    item.append(self.items[i])

        for i in item:    
            i.fellows.pop(tag)

        
        
    def dimension(self):
        self.tmp = []
        self.bind("<Button-1>", self.get_e)
       
    def _del(self, event=None):        
        tags = self.gettags(CURRENT)
        for t in tags:
            if t != "current":
                self.delete(t)
                self.items.pop(t)
                
    def _delete(self, item=None):
        if not item:
            self.bind("<Button-1>", self._del)
        else:
            self.delete(item.tag)
            self.items.pop(item.tag)
                
    
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
        print "Items"
        for kw in self.items:
            print "\t",
            self.items[kw].print_status()
