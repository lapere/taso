import wx
import stackless
# Rely on the wx event loop for a callback.
def waitEvent(item, event):
    notification = stackless.channel()
    item.Bind(event, notification.send)
    notification.receive()
    item.Unbind(event)

# Other command events are sent in a similar fashion.
def clickButton(widget):
    event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED)
    event.SetEventObject(widget)
    widget.ProcessEvent(event)

# This function is picked up by the test framework, and run
# as a stackless tasklet.
def testDialog():
    frame = wx.Frame(None)
    panel = wx.Panel(frame)
    button = wx.Button(panel)

    clickButton(button)
    waitEvent(wx.EVT_CLOSE, frame)

a = wx.App()
testDialog()
a.MainLoop()
