#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx
from cad_canvas import *
from command_line.command_line import CommandLine
#from cad_kernel import *

class MainFrame:

    def __init__(self, parent, id, app):
        self.frame = wx.Frame(parent, id, 'TASO 0.01', size=(600, 400))
        self.menuBar = wx.MenuBar()

        splitter =  wx.SplitterWindow(self.frame, -1)

        self.command_line = CommandLine(splitter)
        sw = wx.ScrolledWindow(splitter, -1, size=(600, 400))
        #panel = wx.Panel(splitter, -1, size=(600, 400))
        self.canvas = cad_canvas(sw, self.command_line.interp)
        self.canvas.app = app
        splitter.SplitHorizontally(sw, self.command_line)
        sw.SetScrollbars(10,10,60,40)
        #self.toolBar = self.frame.CreateToolBar()
        import line
        #self.toolBar.AddSimpleTool(wx.NewId(), line.getBitmap(), "New", "Long help for 'New'")
        #self.toolBar.Realize()

        self.statusBar = self.frame.CreateStatusBar()
        
        menu1 = wx.Menu()
        menu2 = wx.Menu()
        
        self.menuBar.Append(menu1, "&File")
        self.menuBar.Append(menu2, "&Edit")
        
        menu2.Append(wx.NewId(), "&Copy", "Copy in status bar")
        menu2.Append(wx.NewId(), "C&ut", "")
        menu2.Append(wx.NewId(), "Paste", "")
        menu2.AppendSeparator()
        menu2.Append(wx.NewId(), "&Options...", "Display Options")
        
        self.frame.SetMenuBar(self.menuBar)
        self.frame.Show()

__app = wx.PySimpleApp()

frame = MainFrame(parent=None, id=-1, app=__app)
canvas = frame.canvas

del cad_canvas
del CommandLine
del MainFrame
del wx

__app.MainLoop()
