# -*- coding: utf-8 -*-
import wx
from wx import glcanvas
import  wx.lib.dialogs
from OpenGL.GL import *
from OpenGL.GLU import *
import vp

from time import sleep
#from default_tools import *
#from cad_kernel import db
#import tkFileDialog
from math import *
import pickle
from threading import *
import current

class cad_canvas(glcanvas.GLCanvas):

    current = None
    
    def __init__(self, master, **kw):
        glcanvas.GLCanvas.__init__(self, master, -1)
        self.tmp = None
        self.current = None
        self.abort_sema = False
        self.visuals = dict()
        
        self._scale = 1.0


        self.cmd = ""
        self.e = None 
        
        self.origo = 0.0
        self.current_item = None

        self.init = False
        
        # initial mouse position
        self.lastx = self.x = 30
        self.lasty = self.y = 30
        self.xy = []
        
        self.size = self.GetClientSize()
        self.SetSize(master.GetSize())

        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnMouseLeftDouble)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMouseMiddleDown)
        self.Bind(wx.EVT_MIDDLE_UP, self.OnMouseMiddleUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseRightDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnMouseRightUp)
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
        self.repaint()

    def OnMouseLeftDown(self, evt):
        self.xy.append(self.conv_evt_xy(evt))
        self.mouse_state = "left_klick"
        if self.current:
            current.shell.Cut()
            current.shell.AddText(self.visuals[self.current].tag)
    
    def OnMouseLeftUp(self, evt):
        self.ReleaseMouse()

    def OnMouseLeftDouble(self, evt):
        if self.current:
            f = self.visuals[self.current].formula
            current.shell.AddText(".new_formula(\"" + f + "\")")
            
            b_clear = None
            b_enter = None
            def button_close(event = None):
                current.shell.clearCommand()
                b_clear.Destroy()
                b_enter.Destroy()
            def button_enter(event = None):
                cl = current.shell.GetLine(current.shell.GetCurrentLine())
                cl = current.shell.lstripPrompt(cl)
                #current.shell.clearCommand()
                current.shell.run(cl)
                b_enter.Destroy()
                b_clear.Destroy()
            b_clear = wx.Button(current.shell, wx.ID_CLEAR, pos=(0,0))
            b_enter = wx.Button(current.shell, wx.ID_APPLY, pos=(100,0))
            current.shell.Bind(wx.EVT_BUTTON, button_close, id=wx.ID_CLEAR)
            current.shell.Bind(wx.EVT_BUTTON, button_enter, id=wx.ID_APPLY)
            
    
        
    def OnMouseMiddleDown(self, evt):
        self.CaptureMouse()
        self.x, self.y = self.lastx, self.lasty = self.conv_evt_xy(evt)        

    def OnMouseMiddleUp(self, evt):
        self.ReleaseMouse()

    def OnMouseRightDown(self, evt):
        self.abort_sema = True
        self.xy = []
        
    def OnMouseRightUp(self, evt):
        self.abort_sema = False
        self.ReleaseMouse()

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.MiddleIsDown():
            self.lastx, self.lasty = self.x, self.y
            self.x, self.y = self.conv_evt_xy(evt)
            self.Refresh(False)
            
        x,y = self.conv_evt_xy(evt)
        glSelectBuffer(1000) 
        glRenderMode(GL_SELECT)

        glInitNames()
        glPushName(0)
        
        glMatrixMode (GL_PROJECTION)   
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(x-5, x+5, y-5, y+5)
        self.repaint(mode=GL_SELECT)
        glMatrixMode (GL_PROJECTION)
        glPopMatrix()

        b = glRenderMode(GL_RENDER)

        hit = None

        for hit_record in b:
            hit = hit_record[2][0]
            break

        if hit:
            if self.current:
                self.visuals[self.current].passive_color()
                self.visuals[self.current].repaint()
            self.current = hit
            self.visuals[self.current].active_color()
            self.visuals[self.current].repaint()
            self.SwapBuffers()
        elif self.current:
            self.visuals[self.current].passive_color()
            self.visuals[self.current].repaint()
            self.SwapBuffers()
            self.current = None

    def InitGL(self):
        glClearColor(0.97, 0.97, 0.97, 0.0)
        # set viewing projection
        glMatrixMode(GL_PROJECTION)
        glPointSize(6)	
        #glLoadIdentity()
        gluOrtho2D(0.0, self.size.width, 0.0, self.size.height)       

    def repaint(self, mode=None):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        if self.visuals:
            for v in self.visuals:
                self.visuals[v].repaint(mode)
        glPopMatrix()
        
        if self.size is None:
            self.size = self.GetClientSize()
             
        self.SwapBuffers()

    def tag_bind(self, id, name, fun):
        pass

        
    def conv_evt_xy(self, evt):
        x, y = evt.GetPosition()
        vp = glGetIntegerv (GL_VIEWPORT)
        y = vp[3] - y
        return x,y


    def getPoint(self):
        #self.CaptureMouse()
        while not self.xy:
            current.app.Dispatch()
            if self.abort_sema:
                return None
        return self.xy.pop(0)
        
        
        
