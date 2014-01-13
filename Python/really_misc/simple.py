import wx

class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):

        menubar = wx.MenuBar()
        filemenu = wx.Menu()
        viewmenu = wx.Menu()

        self.shst = viewmenu.Append(wx.ID_ANY, 'Show statusbar', 'Show Statusbar', kind = wx.ITEM_CHECK)
        self.shtl = viewmenu.Append(wx.ID_ANY, 'Show toolbar', 'Show toolbar', kind = wx.ITEM_CHECK)

        viewmenu.Check(self.shst.GetId(), True)
        viewmenu.Check(self.shtl.GetId(), True)

        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self.shst)
        self.Bind(wx.EVT_MENU, self.ToggleToolBar, self.shtl)

        menubar.Append(filemenu, '&File')
        menubar.Append(viewmenu, '&View')
        self.SetMenuBar(menubar)

        self.toolbar = self.CreateToolBar()
        self.toolbar.Realize()

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')

        self.SetSize((350,250))
        self.SetTitle('Menus')
        self.Show(True)


    def ToggleStatusBar(self, e):

        if self.shst.IsChecked():
            self.statusbar.Show()
        else:
            self.statusbar.Hide()

    def ToggleToolBar(self, e):

        if self.shtl.IsChecked():
            self.toolbar.Show()
        else:
            self.toolbar.Hide()
            
        
        
        
def main():
    ex = wx.App()
    Example(None)
    ex.MainLoop()

if __name__ == '__main__':
    main()
