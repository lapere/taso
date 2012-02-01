from Tkinter import *
from time import sleep
from default_tools.level import _X,_Y,_A
from default_tools.point import Point
from default_tools.line import Line
from default_tools.cad_kernel import *
import tkFileDialog
from math import *
import pickle

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
        self.items = item.ItemDB()
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

        self.y_0 = _Y(self, 0)
        self.y_e = _Y(self, 600)
        self.x_0 = _X(self, 0)
        self.x_e = _X(self, 800)
        
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

    def getElement(self, event=None):
        self.bind("<Button-1>", self._get_point)
        
        self.sema = True
        self._more = True
        
        while self.sema:

            self.update()
            sleep(0.1)
            
            if not self._more:
                return None
        
        tag = self.get_current()

        if tag[0] in ["X", "Y", "A", "R"]:
            return self.items[tag]

    
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
            elif line.typ() == "a":
                y = self.find_olap("A")
                x = _X(self, self.x)
                print "Plauta",x,y
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

        elif tag[0] in  ["X", "Y", "A"]:
            x = self.find_olap("X")
            y = self.find_olap("Y")
            a = self.find_olap("A")
            for i in [x,y,a]:
                if i:
                    if i.tag[0] != tag[0] or i.tag[0] == "A":
                        p = self.point(self.items[tag], i)
                        return p
            if tag[0] == "X":
                y = _Y(self, self.y)
                p = self.point(self.items[tag], y)
                return p
            if tag[0] == "Y":
                x = _X(self, self.x)
                p = self.point(self.items[tag], x)
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


    def line(self, startp=None, endp=None):
        startp = self.getPoint()
        endp = self.getPoint(rubber=startp)
        Line(self, startp, endp)
        

    def point(self, x, y):
        p = Point(self, x,  y)
        #self.items[p.tag] = p
        return p

    def e_x(self, event=None):
        if not event:
            self.bind("<Button-1>", self.e_x)
        else:
            _X(self, self.canvasx(event.x))
            self.unbind("<Button-1>")
            
    def e_y(self, event=None):
        if not event:
            self.bind("<Button-1>", self.e_y)
        else:
            _Y(self, self.canvasy(event.y))
            self.unbind("<Button-1>")

    def e_p(self, event=None):
        a = self.getElement()
        b = self.getElement()
        self.point(a,b)
        
    def e_a(self):
        a = self.getElement()
        b = self.getElement()
        _A(self, a, b, pi / 4)
        self.items.recalc()
        self.repaint()


    
    def get_e(self, event):
        curr = self.get_current()    

        if curr[0] == "X" or curr[0] == "Y" or curr[0] == "A":
            self.tmp.append(curr)
        
        if len(self.tmp) == 2:
                self.tmp = self.point(self.tmp[0], self.tmp[1])
                self.unbind("<Button-1>")


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

    
    def dimension(self, startp=None, endp=None):
        if startp == None:
            startp = self.getPoint()
        if endp == None:
            endp = self.getPoint(rubber=startp)
            self._more = True
        else:
            self._more = False

        if startp and endp:
            l = Dimension(self, startp, endp)
            self.items[l.tag] = l
        else:
            return

        if self._more:
            self.dimension(startp=endp)

        return l
    
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
            if tag[0] == "X" or tag[0] == "Y":
                self.items[tag].repaint()

        for tag in self.items:
            if tag[0] == "A":
                self.items[tag].repaint()
                
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
        self.items.recalc()
        for kw in self.items:
            print "\t",
            print kw, float(self.items[kw])    
