import os
import wx

class MainWindow(wx.Frame):
        def __init__(self, parent, title):
                wx.Frame.__init__(self, parent, title = title, size = (300, 300))
                self.control = wx.TextCtrl(self, style = wx.TE_MULTILINE)
                self.CreateStatusBar()

                filemenu = wx.Menu()

                menuAbout = filemenu.Append(wx.ID_ABOUT,  "&About", " Information about this program")
                menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")

                menuBar = wx.MenuBar()
                menuBar.Append(filemenu, "&File")
                self.SetMenuBar(menuBar)

                self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
                self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
                
                self.Show(True)

        def OnAbout(self, e):
                dlg = wx.MessageDialog(self, "A small text editor", "About Sample Editor", wx.OK)
                dlg.ShowModal()
                dlg.Destroy()

        def OnExit(self, e):
                self.Close(True)

app = wx.App(False)
frame = MainWindow(None, 'Small Editor')
app.MainLoop()


