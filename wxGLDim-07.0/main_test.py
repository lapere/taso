#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx
import wx.aui
from cad_canvas import cad_canvas
from command_line.command_line import CommandLine
from cad_kernel.db import ItemDB
from default_tools import *
from threading import Thread
import current

class MainFrame:

    def __init__(self, parent, id):
        self.frame = wx.Frame(None, id, 'TASO 0.01', size=(600, 400))
        self.menuBar = wx.MenuBar()

        splitter =  wx.SplitterWindow(self.frame, -1)

        self.command_line = CommandLine(splitter)
        sw = wx.ScrolledWindow(splitter, -1, size=(600, 400))
        self.canvas = cad_canvas(sw)
        

        splitter.SplitHorizontally(sw, self.command_line)
        sw.SetScrollbars(10,10,60,40)
        
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

    def mouse(self, evt):
        print "evt"

current.app = wx.PySimpleApp()

current.mainframe = MainFrame(parent=None, id=-1)
current.canvas = current.mainframe.canvas
current.db = ItemDB(current.mainframe.command_line.interp)
current.shell = current.mainframe.command_line


del cad_canvas
del CommandLine
del MainFrame
del wx
del ItemDB

current.app.MainLoop()
