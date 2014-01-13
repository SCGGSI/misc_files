import Tkinter, Tkconstants, tkFileDialog

class TkFileDialogExample(Tkinter.Frame):

  def __init__(self, root):

    Tkinter.Frame.__init__(self, root)

    self.title = "Test"

    # options for buttons
    button_opt = {'fill': Tkconstants.BOTH, 'padx': 20, 'pady': 20}

    # define buttons
    Tkinter.Button(self, text='Select Files', command=self.askopenfilename).pack(**button_opt)
    Tkinter.Button(self, text='Select a Directory', command=self.askdirectory).pack(**button_opt)

    # define options for opening or saving a file
    self.file_opt = options = {}
    options['defaultextension'] = '.txt'
    options['filetypes'] = [('Workbooks', '.xls*')]
    options['initialdir'] = 'C:\\'
    options['initialfile'] = 'myfile.txt'
    options['parent'] = root
    options['title'] = 'Select workbooks'
    options['multiple'] = 2

    # defining options for opening a directory
    self.dir_opt = options = {}
    options['initialdir'] = 'C:\\'
    options['mustexist'] = False
    options['parent'] = root
    options['title'] = 'This is a title'

  def askopenfilename(self):

    """Returns an opened file in read mode.
    This time the dialog just returns a filename and the file is opened by your own code.
    """

    # get filename
    filename = tkFileDialog.askopenfilename(**self.file_opt)
    

    # open file on your own
    print filename
    print type(filename)
    print len(filename)

  def askdirectory(self):

    """Returns a selected directoryname."""

    print tkFileDialog.askdirectory(**self.dir_opt)

if __name__=='__main__':
  root = Tkinter.Tk()
  root.title("Excel to Delimited")
  TkFileDialogExample(root).pack()
  root.mainloop()
