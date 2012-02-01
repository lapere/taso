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
        self.tmp = None
        self.sema = False
        self.master = ic
        self.visuals = []
        
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

        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMouseMiddleDown)
        self.Bind(wx.EVT_MIDDLE_UP, self.OnMouseMiddleUp)
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

    def OnMouseLeftDown(self, evt):
        self.CaptureMouse()
        x, y = evt.GetPosition()
        vp = glGetIntegerv (GL_VIEWPORT)
        y = vp[3] - y
        self.sema = x,y

    def OnMouseLeftUp(self, evt):
        self.ReleaseMouse()

    def OnMouseMiddleDown(self, evt):
        self.CaptureMouse()
        self.x, y = self.lastx, self.lasty = evt.GetPosition()
        vp = glGetIntegerv (GL_VIEWPORT)
        self.y = vp[3] - y
                

    def OnMouseMiddleUp(self, evt):
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

    def getPoint(self):
        self.sema = None
        self.CaptureMouse()
        while not self.sema:
            wx.Yield()
            sleep(0.01)
        wx.Yield()
        self.ReleaseMouse()
        return self.sema

