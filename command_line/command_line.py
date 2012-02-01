#!/usr/bin/python
# -*- coding: utf-8 -*-
import  wx.py   as  py

class CommandLine(py.shell.Shell):        
    def __init__(self, root):
        py.shell.Shell.__init__(self, root, -1, introText="cad shell")
 

