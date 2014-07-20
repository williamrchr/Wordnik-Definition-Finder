# importing necessary modules
from wordnik import *
import wx
import os

'''

Insert your API key in the api_key variable

you need a wordnik.com developer account to get one

'''

api_url = 'http://api.wordnik.com/v4'
api_key = "b44d5b197c73203bf30040df7ec02ee0c179bbf699b5ca39d"
client = swagger.ApiClient(api_key, api_url)
wordApi = WordApi.WordApi(client)
	

class terminal(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title)
		self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
		self.CreateStatusBar()
		self.Centre()
		filemenu=wx.Menu()
		
		#create Menu Bar
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, "File")
		self.SetMenuBar(menuBar)
		self.Show(True)
		
		#create File Menu
		openfile = filemenu.Append(-1,"Open", "Open your list of words.")
		save = filemenu.Append(-1, "Save", "Save your definitions.")
		
		#bind Events to the menu on click
		self.Bind(wx.EVT_MENU, self.openfile, openfile)
		self.Bind(wx.EVT_MENU, self.savefile, save)
		
	def openfile(self, e): #function to open files
		self.dirname = '' #initialize the directory name
		popup = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN) #opens up the system's file manager and saves the file location to dirname
		if popup.ShowModal() == wx.ID_OK: #on the okay button press
			self.filename = popup.GetFilename() 
			self.dirname = popup.GetDirectory()
			files = open(os.path.join(self.dirname, self.filename), 'r')
			self.words = files.read()
			files.close()
			self.lists = self.read_words(self.words)
			self.body = get_definitions(self.lists)
			self.control.SetValue(self.body)
			
		popup.Destroy()

	def savefile(self,e):
        #saving files
		self.dirname = ''
		popup = wx.FileDialog(self, "Save As...", self.dirname, "", "*.*", wx.SAVE | wx.OVERWRITE_PROMPT)
		if popup.ShowModal() == wx.ID_OK:
			contents = self.control.GetValue()
			self.filename = popup.GetFilename()
			self.dirname = popup.GetDirectory()
			f = codecs.open(os.path.join(self.dirname, self.filename), 'w','utf-8')
			f.write(contents)
			f.close()
			popup.Destroy()
		
	def read_words(self,list):
		list_replace = list.replace("\n", "")
		list_replace = list_replace.replace(",", ", ")
		list_replace = list_replace.replace(",  ", ", ")
		list_split = list_replace.split(", ")
		return list_split
	
def get_definitions(list):
	all_the_definitions = ""
	no_definition = ""
	dlg = wx.ProgressDialog("Progress","How am I doing?", maximum = len(list), style = wx.PD_CAN_ABORT | wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME)
	for word in list:
		
		number_found = list.index(word)
		total = len(list)
		
		(True, skip) = dlg.Update(number_found, ("Found " + str(number_found) + " of " + str(total) + " definitions."))
		
		definitions = wordApi.getDefinitions(word)
		if definitions is None:
			no_definition += (word + "- \n") 
		if definitions is not None:
			all_the_definitions += word + " - \n"
			i = 1
			for definition in definitions:
				all_the_definitions += (str(i) + ". " + definition.text + "\n")
				i+=1
	dlg.Destroy()
	all_the_definitions += ("\n\n\n ----Words not Found---- \n" + no_definition)
	return all_the_definitions
	
#create an instance of the class
app = wx.App(False)
frame = terminal(None, "Will's Definition Finder") #'Will's Definition finder is the default title
app.MainLoop()
