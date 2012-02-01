#!/usr/bin/python
from Tkinter import *
import sys
class Tool:
    toolbox = 100
    def __init__(self, canvas, tool, color, style):
        d = "./tools/"
        self.base_name = d + tool
        self.cursor_str = ('@'+self.base_name+".xbm",
                           self.base_name+".xbm",
                           color, 'white')
        self.home = Tool.toolbox
        self.tag = canvas.create_bitmap(30, Tool.toolbox,
                                        bitmap='@'+self.base_name+"_.xbm",
                                        foreground=color)
        Tool.toolbox +=30
        canvas.tag_bind(self.tag, "<ButtonRelease-1>", self.select_tool)
        canvas.tag_bind(self.tag, "<B1-Motion>", self.move_tool)
        
        self.canvas = canvas
        self.color = color
        self.style = style
        self.oldcursor = self.canvas['cursor']

    def select_tool(self, event):
        c = self.canvas['cursor']
        if c and c[0] != "@" or not c:
            self.canvas.delete(self.tag)
            self.oldcursor = self.canvas['cursor']
            self.canvas['cursor'] = self.cursor_str
            self.canvas.bind("<Button-3>", self.deselect_tool)
            self.canvas.line_style = self.style
            self.canvas.line()
    
    def deselect_tool(self, event):
        self.canvas.bind("<Button-3>", self.canvas.noMore)
        self.canvas.noMore(None)
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        if self.canvas['cursor']:
            self.canvas['cursor'] = self.oldcursor
            self.tag = self.canvas.create_bitmap(x + 20,
                                                 y + 20,
                                                 bitmap="@"+self.base_name+"_.xbm",
                                                 foreground=self.color)
            self.canvas.tag_bind(self.tag, "<ButtonRelease-1>", self.select_tool)
            self.canvas.tag_bind(self.tag, "<B1-Motion>", self.move_tool)
        
    def move_tool(self, event):
        self.canvas.tag_bind(self.tag, "<ButtonRelease-1>", self.do_not_select)
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.tag, x, y)

    def do_not_select(self, event):
        self.canvas.tag_bind(self.tag, "<ButtonRelease-1>", self.select_tool)

    def repaint(self, event=None):
        x = self.canvas.canvasx(30)
        y = self.canvas.canvasy(self.home)
        self.canvas.coords(self.tag, x, y)
        
class EngineeringPencils:

    def __init__(self, canvas):
        self.pen_param = dict(black="0.25m",
                          yellow="0.35m",
                          brown="0.5m",
                          blue="0.7m",
                          orange="1m",
                          green="1.4m",
                          gray="2m")
        self.pen = []
        for pen in self.pen_param:
            if pen == "yellow":
                color = "#ee1"
            elif pen == "green":
                color ="#0e1"
            else:
                color = pen
            self.pen.append(Tool(canvas, pen, color, self.pen_param[pen]))
        


if __name__ == '__main__':          
    c = Canvas(width=400, height=600)
    c.pack()
    p = EngineeringPencils(c)
    c.mainloop()
