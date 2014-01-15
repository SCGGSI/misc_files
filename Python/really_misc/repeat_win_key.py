from threading import Thread
from time import sleep
from win32com.client import Dispatch

shell = Dispatch("WScript.Shell")

def repeat_win():
	while True:
		shell.SendKeys("^{ESC}")
		sleep(1)

repeat_win()
