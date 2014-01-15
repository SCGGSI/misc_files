import sys
import os
from win32com.client import Dispatch

OutApp = Dispatch("Outlook.Application")
OutMail = OutApp.CreateItem(0)

wd = os.getcwd()

address_book = {'declan' : 'decummings@deloitte.com',
		'kyle' : 'kypeterson@deloitte.com'}

attachment = wd + '\\' + str(sys.argv[2])
recipient = str(sys.argv[1]).lower()

OutMail.To = address_book[recipient]
OutMail.Attachments.Add(attachment)
OutMail.Send()

print "Email sent."
