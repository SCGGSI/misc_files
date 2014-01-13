import wx
import os

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title = title, size = (300, 300))
        self.control = wx.TextCtrl(self, style = wx.TE_MULTILINE)
        self.CreateStatusBar()

        filemenu = wx.Menu()
        editmenu = wx.Menu()

        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", " Information about this program.")
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", "Open a file.")
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")

        menuUndo = editmenu.Append(wx.ID_UNDO, "&Undo", " Undo previous command")
        menuRedo = editmenu.Append(wx.ID_REDO, "&Redo", " Redo previous undo")

        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")
        menubar.Append(editmenu, "&Edit")

        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        self.Bind(wx.EVT_MENU, self.OnUndo, menuUndo)
        self.Bind(wx.EVT_MENU, self.OnRedo, menuRedo)
        
        self.Show(True)

    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "A small text editor \nfor testing", "About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnOpen(self, e):
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.txt", wx.OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()

            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()

        dlg.Destroy()

    def OnExit(self, e):
        self.Close(True)

    def OnUndo(self, e):
        dlg = wx.MessageDialog(self, "Not available yet.", "Undo", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnRedo(self, e):
        dlg = wx.MessageDialog(self, "Not available yet.", "Redo", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()


app = wx.App(False)
frame = MainWindow(None, "Testing Menus")
app.MainLoop()
    
