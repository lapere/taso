
import  wx

#---------------------------------------------------------------------------

class MySplitter(wx.SplitterWindow):
    def __init__(self, parent, ID):
        wx.SplitterWindow.__init__(self, parent, ID,
                                   style = wx.SP_LIVE_UPDATE
                                   )
        
#---------------------------------------------------------------------------

app = wx.App()
f = wx.Frame(None, -1)

splitter = MySplitter(f, -1)

sty = wx.BORDER_SUNKEN

p1 = wx.Window(splitter, style=sty)
p1.SetBackgroundColour("pink")
wx.StaticText(p1, -1, "Panel One", (5,5))

p2 = wx.Window(splitter, style=sty)
p2.SetBackgroundColour("sky blue")
wx.StaticText(p2, -1, "Panel Two", (5,5))

splitter.SetMinimumPaneSize(20)
splitter.SplitVertically(p1, p2, -100)

        

app.MainLoop()
