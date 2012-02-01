from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import wx
from wx import glcanvas
import sys

x = y = 0 # to store mouse loc


class FpsTimer(wx.Timer):
    def __init__(self, fps, f):
        wx.Timer.__init__(self)
        self.Start(1000./fps)
        self.f = f # function to call on notify

    def Notify(self): self.f()



class MwxFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, title='frametitle', pos=(0,0), size=(20,20)):
        wx.Frame.__init__(self, parent, id, title, pos, size)
        self.SetSize(size)
        
    def domenu(self):
        # menu bar
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        menuBar.Append(menu1,"&File")
        menu1.Append(101, "&New", "new file")
        menu1.AppendSeparator()
        menu1.Append(105, "&Quit", "quit")
        self.SetMenuBar(menuBar)
        # status bar
##        self.CreateStatusBar(1,0)
##        self.SetStatusText("status bar")
       
    def structure(self, canvas):
        self.domenu()
        
        bodyupSizer = wx.BoxSizer(wx.VERTICAL)

        #bodydownSizer = wx.BoxSizer(wx.HORIZONTAL)
        
##        bodyupSizer.Add(canvas, 0, wx.GROW | wx.ALL | wx.ALIGN_RIGHT, 0)
##        canvas.SetSize(canvas.GetBestSize()) # !!!!!
        
        bodyupSizer.Add(canvas, 0) # , wx.LEFT, 1)

        #bodyupSizer.Add(bodydownSizer, 0, wx.GROW|wx.ALL|wx.ALIGN_RIGHT, 50)

        self.SetAutoLayout(True)
        self.SetSizer(bodyupSizer)
        self.Layout()
        self.Centre()




        
class App(wx.App):
    def __init__(self, pos, size):
        wx.App.__init__(self, 0)
        self.name = "testing wxopengl"
        self.size = size
        self.pos = pos
        self.init = 0
        # correcting glcanvas size to acomodate to frame space left by other widgets
        f = size[0], size[1]+22
        self.frame = MwxFrame(None, -1, self.name, self.pos, f)#self.size) #wxframe
        
        self.size = self.size[0], self.size[1] + 27 # 28 with menu, 54 with status bar on linux

        self.canvas = glcanvas.GLCanvas(self.frame, -1, self.pos, self.size)

        #self.canvas.SetSize(self.size)
        self.canvas.Bind(wx.EVT_PAINT, self.paint)
        def void(self) : pass # a dummy function
        self.canvas.Bind(wx.EVT_ERASE_BACKGROUND, void) # dummy to avoid flash on windows
        self.canvas.Bind(wx.EVT_MOTION, self.onMouseMoved)
        
        #print self.frame.GetClientSize(), self.size[1] - 46
        
        self.glsize = self.canvas.GetSize() # passed to glOrtho
        #print 'glsize, size, framesize', self.glsize, self.size, self.frame.GetClientSize()
        
        self.frame.structure(self.canvas)
        self.frame.Show()
        
    def onMouseMoved(self, evt):
        global x,y
        x,y = evt.GetPosition()

    def initGL(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glOrtho(0, self.glsize[0], self.glsize[1], 0, 1, 0) # map gl units to pixels
##        glOrtho(-1, self.glsize[0], self.glsize[1]+1, 0, 1, 0) # map gl units to pixels

        glMatrixMode(GL_MODELVIEW)
        # now init timer
        self.t = FpsTimer(20, self.canvas.Refresh)
        self.init = True
##        glDepthMask(GL_FALSE)


    def paint(self,event):
        #print x,y
        wx.PaintDC(self.canvas)
        self.canvas.SetCurrent()
        if not self.init : self.initGL()
        glClearDepth(1.0)
        glClearColor(1,1,1, 1) #bg color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

##        glBegin(GL_QUADS)
##        glColor3f(0,0,1) #
##        glVertex3f(100, 100, 0) #left top
##        glVertex3f(700, 100, 0)
##        glVertex3f(700, 500, 0)
##        glVertex3f(100, 500, 0)
##        glEnd()
	
        glPushMatrix()
        glTranslate(x,y, 0) # go to mouseloc
        glBegin(GL_QUADS)
        glColor3f(0.8,0,0) #
        glVertex3f(-10, 10, 0) #left top
        glVertex3f(10, 10, 0)
        glVertex3f(10, -10, 0)
        glVertex3f(-10, -10, 0)
        glEnd()
        glPopMatrix()	
        
       # red diagonal lines from vertex of window
        glBegin(GL_LINE_LOOP)
        glColor3f(1,0,0) #
        glVertex2i(0,0)
        glVertex2i(self.size[0], self.size[1])
        glVertex2i(0, self.size[1])
        glVertex2i(self.size[0], 0)
        glVertex2i(0,0) # marquee
        glVertex2i(self.size[0], 0)
        glVertex2i(self.size[0], self.size[1])
        glVertex2i(0, self.size[1])
        glEnd() # end line loop
				
        self.canvas.SwapBuffers()


def main():
    app = App((0,0), (800,600)) # pos and size
    app.MainLoop()


if __name__ == '__main__':
    main()

