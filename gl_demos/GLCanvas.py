
import wx
import sys
from wx import glcanvas 
from OpenGL.GL import *
from OpenGL.GLU import *
import time

contours = dict()

        
class Point:
    cnt = 0
    def __init__(self, x, y):
        Point.cnt += 1
        self.x = x
        self.y = y
        self.name = Point.cnt
        self.color = [0.2, 0.2, 0.2]
        self.create_visibles()
        glFinish()

    def create_visibles(self):
        glColor3f(*self.color)
        glBegin(GL_POINTS)
        glVertex2fv((self.x, self.y))
        glEnd()

    def repaint(self, mode=None):
        if mode == GL_SELECT:
            glLoadName(self.name)
        self.create_visibles()

    def move(self, x, y):
        vp = glGetIntegerv (GL_VIEWPORT)
        self.x = x
        self.y = vp[3] - y
        glClear( GL_COLOR_BUFFER_BIT )
        for i in contours:
            contours[i].repaint()
        glFinish()

    def active(self):
        self.color = [1.0, 0.0, 0.0]
        
    def passive(self):
        self.color = [0.2, 0.2, 0.2]

        
ID_START = wx.NewId()

class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1)
        wx.Button(self, ID_START, 'Point')
        self.Bind (wx.EVT_BUTTON, self.OnStart, id=ID_START)
        self.c = Canvas(self)
        self.c.Show()

    def OnStart(self, event):
        self.c.x = 0
        while True:
            if self.c.x != 0:
                self.c.point(self.c.x, self.c.y)
                return
            else:
                time.sleep(0.01)
                wx.Yield()
            



class Canvas(glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1, size=(200,200), pos=(0,100))
        self.init = False

        # initial mouse position
        self.lastx = self.x = 30
        self.lasty = self.y = 30
        self.size = self.GetClientSize()
        
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        

    def OnEraseBackground(self, event):
        pass # Do nothing, to avoid flashing on MSW.

    def OnSize(self, event):
        size = self.size = self.GetClientSize()
        if self.GetContext():
            self.SetCurrent()
            glViewport(0, 0, size.width, size.height)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0.0, size.width, 0.0, size.height)
        event.Skip()
        print size.width, size.height

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent()
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()


    def OnMouseDown(self, evt):
        self.CaptureMouse()
        self.x, self.y = self.lastx, self.lasty = evt.GetPosition()
        vp = glGetIntegerv (GL_VIEWPORT)
        self.y = vp[3] - self.y

    def point(self, x, y):
        p = Point(x, y)
        contours.update({p.name:p})
        self.OnPaint(None)
   
    def OnMouseUp(self, evt):
        self.ReleaseMouse()

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            self.lastx, self.lasty = self.x, self.y
            self.x, self.y = evt.GetPosition()
            self.Refresh(False)


    def InitGL(self):
        glClearColor( 0.8, 0.8, 0.8, 0.0 )
        glPointSize(6)
        

    def OnDraw(self):
        glClear( GL_COLOR_BUFFER_BIT )
        for i in contours:
            contours[i].repaint()
        glFinish()
        self.SwapBuffers()

        
a = wx.App()
p = MainFrame(None)

p.Show()
a.MainLoop()
