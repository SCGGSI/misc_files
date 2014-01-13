import wx

class Example(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):
        toolbar = self.CreateToolBar()
        qtool = toolbar.AddLabelTool(wx.ID_ANY, 'Quit')
        toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.OnQuit, qtool)

        self.SetSize((250,200))
        self.Show(True)

    def OnQuit(self, e):
        self.Close()

ex = wx.App()
Example(None)
ex.MainLoop()
