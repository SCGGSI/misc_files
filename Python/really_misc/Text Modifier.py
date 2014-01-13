import wx
import os
import datetime

filetype = "SAS Log (*.log)|*.log|Allfiles (*.*)|*.*"

class MainWindow(wx.Frame):
    sas_log = ''
    dirname = ''
    filename = ''
    file_opened = False
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title = title, size = (500, 500))

        self.panel = wx.Panel(self)
        self.SetBackgroundColour('white')
        
        # self.control = wx.TextCtrl(self, style = wx.TE_MULTILINE)
        self.CreateStatusBar()

        filemenu = wx.Menu()
        logmenu = wx.Menu()
        editmenu = wx.Menu()

        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", \
                                    " Information about this program.")
        
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", "Open a file.")
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", \
                                   " Terminate the program")

        menuDefault = logmenu.Append(wx.ID_APPLY, "&Default values", \
                                     "Searches for NOTE:, WARNING:, and "\
                                     "ERROR: and stores values in new files.")

        menuUndo = editmenu.Append(wx.ID_UNDO, "&Undo", \
                                   " Undo previous command")
        
        menuRedo = editmenu.Append(wx.ID_REDO, "&Redo", " Redo previous undo")

        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")
        menubar.Append(logmenu, "&Log")
        menubar.Append(editmenu, "&Edit")

        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        self.Bind(wx.EVT_MENU, self.SearchLog, menuDefault)

        self.Bind(wx.EVT_MENU, self.OnUndo, menuUndo)
        self.Bind(wx.EVT_MENU, self.OnRedo, menuRedo)
        
        self.Show(True)

    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "A SAS log cleanser for reviewing", \
                               "About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnOpen(self, e):
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", \
                            filetype, wx.OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()

            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.sas_log = f.readlines()
            f.close()

        dlg.Destroy()

        self.file_opened = True

    def OnExit(self, e):
        self.Close(True)

    def SearchLog(self, e):
        if self.file_opened:
            write_file = self.filename.split(".")[0]
            now = datetime.datetime.now()
            write_file += " %d%d%d %d%d%d.log" % (now.month, now.day, now.year, \
                                                  now.hour, now.minute, now.second)

            f = open(os.path.join(self.dirname, write_file), 'w')

            for line in self.sas_log:
                values = ['NOTE:', 'WARNING:', 'ERROR:']
                if any(val for val in values):
                    f.write(line)
                    
            f.close()
            del self.sas_log
            self.file_opened = False

        else:
            dlg = wx.MessageDialog(self, "You must open a log first.", \
                                   "Warning", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()

    def OnUndo(self, e):
        dlg = wx.MessageDialog(self, "Not available yet.", "Undo", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnRedo(self, e):
        dlg = wx.MessageDialog(self, "Not available yet.", "Redo", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()


app = wx.App(False)
frame = MainWindow(None, "Log cleanser")
app.MainLoop()
    
