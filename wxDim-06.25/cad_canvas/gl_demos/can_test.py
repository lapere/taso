
import wx
import sys
from wx import glcanvas

from OpenGL.GL import *
from OpenGL.GLU import *


class CanvasBase(glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1)
        self.init = False
        # initial mouse position
        self.lastx = self.x = 30
        self.lasty = self.y = 30
        self.z = 1.0
        self.size = self.GetClientSize()
        self.SetSize(parent.GetSize())

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_MIDDLE_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_MOUSEWHEEL, self.MouseWheel)

    def MouseWheel(self, evt):
        if evt.WheelRotation > 0:
            self.z *= 0.9
        else:
            self.z *= 1.1
        
        self.Refresh(False)
        

    def OnSize(self, event):
        print "size"
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


    def OnMouseUp(self, evt):
        self.ReleaseMouse()

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.MiddleIsDown():
            self.lastx, self.lasty = self.x, self.y
            self.x, y = evt.GetPosition()
            vp = glGetIntegerv (GL_VIEWPORT)
            self.y = vp[3] - y
            self.Refresh(False)
            
        
    def InitGL( self ):
        self.SetCurrent()
        glMatrixMode(GL_PROJECTION)
        gluOrtho2D(0.0, self.size.width, 0.0, self.size.height)     	
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPointSize(2)
        

    def OnDraw(self):
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glTranslate((self.x - self.lastx), (self.y - self.lasty), 0.0)

        glPushMatrix()
        glColor3f(0.9, 0.2, 0.0)
        glScalef(self.z, self.z, 0.0)

        glBegin(GL_POINTS)
        for x in range(300):
            for y in range(300):        
                 glVertex2fv((float(x), float(y)))
        glEnd()
        glPopMatrix()
    

        self.SwapBuffers()



__app = wx.PySimpleApp()
frame = wx.Frame(None, -1, 'TASO 0.01', size=(600, 400))
panel = wx.Panel(frame, -1, size=(600, 400))
c = CanvasBase(panel)
c.InitGL()
frame.Show()
__app.MainLoop()


