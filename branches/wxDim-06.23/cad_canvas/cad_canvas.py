# -*- coding: utf-8 -*-
import wx
from wx import glcanvas
import  wx.lib.dialogs
from OpenGL.GL import *
from OpenGL.GLU import *
import vp

from time import sleep
from default_tools import *
from cad_kernel import db
import tkFileDialog
from math import *
import pickle
from threading import *

class cad_canvas(glcanvas.GLCanvas):

    current = None
    
    def __init__(self, master, ic, **kw):
        glcanvas.GLCanvas.__init__(self, master, -1)
        self.app = None
        self.sema = Event()
        self.x = None
        self.y = None
        self.mx = None
        self.my = None
        
        self.dim = None
        self.tmp = None
        self.items = db.ItemDB(ic)
        self.visuals = []
        self.id = None
        self.panx = 0
        self.panx = 0
        self.lastx = 0
        self.lasty = 0
        self._scale = 1.0


        self.cmd = ""
        self.e = wx.TextEntryDialog(self, 'Syötä uusi arvo tai kaava')
        
        self.origo = 0.0
        self.current_item = None

        self.init = False
        
        # initial mouse position
        self.lastx = self.x = 30
        self.lasty = self.y = 30
        
        self.size = self.GetClientSize()
        self.SetSize(master.GetSize())
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        
                
    def OnSize(self, event):
        size = self.size = self.GetClientSize()
        if self.GetContext():
            self.SetCurrent()
            glViewport(0, 0, size.width, size.height)
        event.Skip()


    def OnPaint(self, event):
        
        self.SetCurrent()
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()


    def OnMouseDown(self, evt):
        self.CaptureMouse()
        self.x, y = self.lastx, self.lasty = evt.GetPosition()
        vp = glGetIntegerv (GL_VIEWPORT)
        self.y = vp[3] - y
        
        print self.x, self.y

    def th(self):
        while True:
            print self.x
            if self.x:
                return
            sleep(1)
            

    def OnMouseUp(self, evt):
        self.ReleaseMouse()

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.MiddleIsDown():
            self.lastx, self.lasty = self.x, self.y
            self.x, y = evt.GetPosition()
            vp = glGetIntegerv (GL_VIEWPORT)
            self.y = vp[3] - y
            self.Refresh(False)
            

    def InitGL(self):
        # set viewing projection
        
        glMatrixMode(GL_PROJECTION)
        glPointSize(6)	
        #glLoadIdentity()
        gluOrtho2D(0.0, self.size.width, 0.0, self.size.height)       

    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        for v in self.visuals:
            v.repaint()
        glPopMatrix()
        
        if self.size is None:
            self.size = self.GetClientSize()
             
        self.SwapBuffers()

    def tag_bind(self, id, name, fun):
        pass

    ### Old stuff ---
        
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

    def shot(self):
        print "Shot!"
    
    def get_point(self):
        self.x = 0
        t = Thread(group=None, target=self.th)
        t.start()
        t.join()

        #self.t.join()
        return self.x , self.y
            
    
    
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
        p = vp.Point(self, x, y, 0)
        self.visuals.append(p)
        return p
        
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


