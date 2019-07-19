from testing_GUI import TestingFrame
import intake
import wx, pickle, gettext, json, os
from tinydb import TinyDB, Query, where

COLOR ={"light":{"fg":"#000000", 'bg':'#ffffff'}, \
		'dark':{"fg":"#ffffff", 'bg':'#080808'}}

class TFrame(TestingFrame):
	class Data():
		"""
		Used to be able to save data to/from a file
		"""
		def __init__(self):
			self.pathname = ''
			self.issue_summary = ''
			self.user = ''
			
	def __init__(self, *args, **kwds):
		import glob
		TestingFrame.__init__(self,*args, **kwds)
		uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])
		files = glob.glob(uppath(__file__, 1) + os.sep + "*.xlsx")
		self.root_path = uppath(__file__,1)
		self.settings = {}
		self.dark = False
		
		database = []
		self.dbfile = ""
		self.excel_filename = ""
		self.load_settings()
		
		inpt = intake.read_xlsx(self.root_path + os.sep + self.excel_filename)
		for sheet in inpt:
			for row in sheet:
				database.append(row)
		intake.build_db(database, self.root_path + os.sep+ self.dbfile)
		self.db = TinyDB(self.root_path + os.sep+ self.dbfile)
		self.Issue = Query()
		
		self.search_dict = \
		{intake.USER_TYPE: self.choice_user,
		intake.CATEGORY: self.choice_component,
		intake.BEST_PRACTICE: self.choice_best_practice,
		intake.PLATFORM: self.choice_platform,
		intake.WCAG: self.choice_wcag}
		
		for label, choice in self.search_dict.items():
			list_items = self.get_column_names(label)
			list_items.sort()
			choice.AppendItems(list_items)
		
		self.choices = []
		self.choices.append(self.choice_platform)
		self.choices.append(self.choice_user)
		self.choices.append(self.choice_severity)
		self.choices.append(self.choice_component)
		self.choices.append(self.choice_best_practice)
		self.choices.append(self.choice_wcag)
			
		self.isDirty = False #used to save the state of changes
		self.data = TFrame.Data()
		self.name = " - TTT"
		self.setTitle("Untitled")
		
		self.important = []
		self.important.append(self.choice_user)
		self.important.append(self.choice_platform)
		self.important.append(self.text_ctrl_issue_summary)
		self.important.append(self.text_ctrl_issue_description)
		self.important.append(self.text_ctrl_steps_to_reproduce)
		self.important.append(self.text_ctrl_remediation)
		self.important.append(self.choice_severity)
		self.important.append(self.choice_component)
		self.important.append(self.choice_best_practice)
		self.important.append(self.choice_wcag)
		
		root = self.tree_ctrl_1.AddRoot("All Issues")
		colorBlind = self.tree_ctrl_1.AppendItem(root,"Color Blind")
		screenReader = self.tree_ctrl_1.AppendItem(root,"Screen Reader")
		contrast = self.tree_ctrl_1.AppendItem(colorBlind,"Improve Contrast")
		labels = self.tree_ctrl_1.AppendItem(screenReader,"Add Labels")

	def setDirty(self, isDirty):
		"""
		Marks the current work as different/same from the saved file
		"""
		self.isDirty = isDirty
		title = self.GetTitle()
		if isDirty and not title[0] == '*':
			self.SetTitle('* ' + title)
		elif not isDirty and title[0] == '*':
			self.SetTitle(title[2:])
	
	def setTitle(self, title):
		"""
		Sets the title of the window to the file pathname
		"""
		if self.isDirty:	
			foo = '* ' + title + self.name
		else:
			foo = title + self.name
		self.SetTitle(foo)
	
	def on_menu_new(self, event): 
		"""
		Called on file>new or ctrl+n
		"""
		if not self.safeToQuit():
			return
		self.data = TFrame.Data()
		self.setTitle("Untitled")
		self.setDirty(False)
		for elem in self.important:
			if type(elem) == type(wx.Choice):
				elem.SetSelection(0)
			elif type(elem) == type(wx.TextCtrl):
				elem.SetValue('')

	def on_menu_open(self, event):
		"""
		Called on file>open or ctrl+o
		"""
		if not self.safeToQuit():
			return
		
		filename = ''
		with wx.FileDialog(self, message="Open a file",	wildcard="RPT  Files (*.rpt)|*.rpt", style=wx.FD_OPEN |wx.FD_FILE_MUST_EXIST) as dlg:
		
			if dlg.ShowModal() == wx.ID_OK:
				filename = dlg.GetPath()
			
			if filename:
				with open(filename,'rb') as f:
					self.data = pickle.load(f)
					f.close()
					self.text_ctrl_data.ChangeValue(str(self.data.__dict__))
					self.text_ctrl_issue_summary.SetValue(self.data.issue_summary)
					self.choice_user.SetSelection(self.data.user)
					self.setTitle(get_name_from_file(filename))
				self.setDirty(False)
			else:
				print("No file selected")

	def on_menu_save(self, event):  # wxGlade: TestingFrame.<event_handler>
		"""
		Called on file>save or ctrl+s
		"""
		if self.data.pathname == "":
			self.on_menu_save_as(event)
		else:
			self.save_as(self.data.pathname)
	
	def on_menu_save_as(self, event):
		"""
		Called on file>save_as or ctrl+shift+s
		"""
		with wx.FileDialog(self, "Save RPT file", wildcard="RPT files (*.rpt)|*.rpt", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return     # the user changed their mind

			# save the current contents in the file
			pathname = fileDialog.GetPath()
			self.save_as(pathname)
			
	def save_as(self, pathname):
		"""
		does the work for both on_menu_save_as and on_menu_save
		"""
		with open(pathname, 'wb') as file:
			self.setTitle(get_name_from_file(pathname))
			self.data.pathname = pathname
			self.data.issue_summary = self.text_ctrl_issue_summary.GetValue()
			self.data.user = self.choice_user.GetSelection()
			
			self.doSaveData(file)
			file.close()

	def doSaveData(self, file):
		"""
		Does the actual work of saving
		"""
		self.setDirty(False)
		pickle.dump(self.data, file, pickle.HIGHEST_PROTOCOL)
		
	def on_menu_import(self, event):  # wxGlade: TestingFrame.<event_handler>
		"""
		Called when importing a report. Possibly used by managers (not implemented)
		"""
		print("Event handler 'on_menu_import' not implemented!")
		event.Skip()

	def on_menu_export_pdf(self, event):  # wxGlade: TestingFrame.<event_handler>
		"""
		Generates a word doc to be used for a PDF output
		"""
		print("Event handler 'on_menu_export_pdf' not implemented!")
		event.Skip()

	def on_menu_export_excel(self, event):  # wxGlade: TestingFrame.<event_handler>
		"""
		Generates an excel doc of all issues.  possibly used to upload to JIRA
		"""
		print("Event handler 'on_menu_export_excel' not implemented!")
		event.Skip()

	def on_menu_exit(self, event):  # wxGlade: TestingFrame.<event_handler>
		"""
		Called on file>exit or alt+f4
		"""
		if not self.safeToQuit():
			return
		self.Close()
		
	def on_menu_about(self, event):
		"""
		Used to learn about the program e.g. version number...
		"""
		self.aboutFrame.show()
		
	def on_menu_dark(self, event):
		"""
		Used to turn on/off dark mode
		"""
		self.dark = bool(event.Selection)
		widgets = getWidgets(self)
		for widget in widgets:
			if "SetBackgroundColour" in dir(widget):
				if self.dark:
					color = "dark"
				else:
					color = "light"
				
				widget.SetBackgroundColour(COLOR[color]['bg'])
				widget.SetForegroundColour(COLOR[color]['fg'])
		self.Refresh()
		event.Skip()

	def on_choice_platform(self, event):  # wxGlade: TestingFrame.<event_handler>
		self.update_search()
		platform_int = self.choice_platform.GetSelection()
		platform = self.choice_platform.GetString(platform_int)
		self.db.search(self.Issue.Platform == platform)
		self.setDirty(True)
		event.Skip()

	def on_choice_user(self, event):  # wxGlade: TestingFrame.<event_handler>
		self.update_search()
		user_type_int = self.choice_user.GetSelection()
		user_type = self.choice_user.GetString(user_type_int)
		self.db.search(self.Issue.UserType == user_type)
		self.setDirty(True)
		event.Skip()

	def on_choice_priority(self, event):  # wxGlade: TestingFrame.<event_handler>
		self.update_search()
		self.setDirty(True)
		event.Skip()

	def on_choice_component(self, event):  # wxGlade: TestingFrame.<event_handler>
		self.update_search()
		self.setDirty(True)
		event.Skip()

	def on_choice_best_preactice(self, event):  # wxGlade: TestingFrame.<event_handler>	
		self.update_search()
		self.setDirty(True)
		event.Skip()

	def on_choice_wcag(self, event):  # wxGlade: TestingFrame.<event_handler>
		self.update_search()
		self.setDirty(True)
		#wcag_selection = self.choice_wcag.choices[event.GetSelection()]
		selection = (self.choice_wcag.GetString(event.GetSelection()))
		if selection == "All":
			self.text_ctrl_wcag.SetValue("")
		results = self.db.search(self.Issue[intake.WCAG] == selection)
		if len(results):
			self.text_ctrl_wcag.SetValue(results[0][intake.LINK])
			
	def on_text_issue_summary(self, event):
		self.setDirty(True)
		event.Skip()
		
	def safeToQuit(self):
		"""
		determines if there is unsaved work or if the user is ok with trashing changes
		"""
		if self.isDirty:
			result = (wx.MessageBox("You have unsaved work. Are you sure you want to exit?", "Really exit?", wx.ICON_QUESTION | wx.YES_NO, self) == wx.YES)
			return result
		else:
			return True
	
	def on_notebook_page_changed(self, event):  # wxGlade: TestingFrame.<event_handler>
		if event.GetSelection() == 3:
			self.text_ctrl_data.ChangeValue(str(self.data.__dict__))
		elif event.GetSelection() == 1:
			dd = dict()
			for k, v in self.search_dict.items():
				selection = self.get_choice_string(v)
				if not selection == "All":
					dd[k] = selection
			result = self.compound_search(dd)
			count = len(result)
			self.text_ctrl_count.ChangeValue(str(count))
			
	def on_tree_key_down(self, event):  # wxGlade: TestingFrame.<event_handler>
		if event.GetKeyCode() == 395: #Applications key
			for func in dir(event):
				print(func)
			print(event.GetSelection())
		event.Skip()
		
	def on_tree_item_activated(self, event):  # wxGlade: TestingFrame.<event_handler>
		
		event.Skip()

	def on_tree_sel_changed(self, event):  # wxGlade: TestingFrame.<event_handler>
		id = self.tree_ctrl_1.GetFocusedItem()
		if self.dark:
			print(self.tree_ctrl_1.SetItemBackgroundColour(id, COLOR['dark']['fg']))
			print('dark')
		event.Skip()
	
	def get_column_names(self, column_title):
		"""
		Given a key, return all possible values, as a list
		"""
		result = self.db.search(self.Issue)
		user_types = list(set([item[column_title] for item in result[1:]]))
		return user_types
		
	def update_search(self):
		for string, choice in self.search_dict.items():
			selection = choice.GetString(choice.GetSelection())
			#print(string + ": " + selection)
			
			#remove the current option from the dict for the search
			copy_string_dict = dict()
			for k,v in self.search_dict.items():
				if not "All" == self.get_choice_string(v):
					copy_string_dict[k] = self.get_choice_string(v)
					
			if string in copy_string_dict:
				try:
					del copy_string_dict[string]
				except KeyError:
					pass
			#print("copy string dict:\t"+str(copy_string_dict))
			results = self.compound_search(copy_string_dict)
			#print("len(results):\t"+str(len(results)))
			list_to_append = []
			#print("results[0]:\t" + str(results[0]))
			#print("string:\t"+ string)
			for item in results:
				#print(item[k])
				list_to_append.append(item[string])
			list_to_append = list(set(list_to_append))
			self.reset_choices(choice,list_to_append)
		
	def get_choice_string(self,choice):
		selection_int = choice.GetSelection()
		return choice.GetString(selection_int)

	def compound_search(self, dd):
		"""
		given a dictionary of search terms, returns a list of the results
		"""
		result = []
		to_delete = []
		for k,v in dd.items():
			if (v == "") or (v =="ALL"):
				to_delete.append(k)
		for key in to_delete:
			try:			
				del dd[key]
			except KeyError:
				pass
		#print("Filtering based on:\t" + str(dd))
		if dd:
			search_list = []
			for k,v in dd.items():
				search_list.append("(self.Issue."+k+" == '"+v+"')")
			code = "self.db.search("+'&'.join(search_list)+")"
			result = eval(code)
		else:
			result = self.db.search(self.Issue)
		return result
		
	def reset_choices(self,choice, choices):
		current = self.get_choice_string(choice)
		choice.Clear()
		choice.AppendItems(["All"])
		choices = list(set(choices))
		choices.sort()
		#print("choices:")
		#print(choices)
		choice.AppendItems(choices)
		#print(choice.choices)
		sel_int = choice.FindString(current)
		#print(sel_int)
		choice.SetSelection(sel_int)
	
	def load_settings(self):
		settings_file = self.root_path + os.sep + "settings.txt"
		try:
			f = open(settings_file, 'wt')
			string = f.read()
		except IOError:
			f = open(settings_file, 'wt')
			string = '{"dark": False, "dbfile":"db.json", "excel_filename":""}'
		finally:
			if string:
				try:
					settings_handler = eval(string)
					if not type(settings_handler) == type(dict()):
						raise KeyError
				except:
					settings_handler = {'dark': False, "dbfile":"db.json", "excel_filename":""}
			else:
				settings_handler = {'dark': False, "dbfile":"db.json", "excel_filename":""}
				
			#dark
			try:
				self.settings['dark'] = settings_handler['dark']
			except KeyError:
				self.settings['dark'] = False
			#database file
			try:
				self.dbfile = settings_handler['dbfile']
			except KeyError:
				self.dbfile = "db.json"
			
			#excel source
			try:
				self.excel_filename = settings_handler['excel_filename']
				if self.excel_filename == "":
					raise KeyError
			except KeyError:
				with wx.FileDialog(self, message="Select an Excel file of the Issue table",	wildcard="Excel  Files (*.xlsx)|*.xlsx", style=wx.FD_OPEN |wx.FD_FILE_MUST_EXIST) as dlg:
					if dlg.ShowModal() == wx.ID_OK:
						filename = dlg.GetPath()
						if filename:
							self.excel_filename = (filename.split(os.sep))[-1]
					else:
						print("No file selected")
			string = str({'dark': self.dark, 'dbfile': self.dbfile, 'excel_filename':self.excel_filename})
			f.write(string)
			f.close()
		
def remove_key(dd, key):
	r = dict(dd)
	del r[key]
	return r

def get_name_from_file(file):
	"""
	Given a full file path C:/one/foo.rpt returns foo
	Used to get the title of the window
	"""
	broken_file = file.split(os.sep)
	return (broken_file[-1][:-4])

def getWidgets(parent):
	"""
	Return a list of all the child widgets
	"""
	items = [parent]
	for item in parent.GetChildren():
		items.append(item)
		if hasattr(item, "GetChildren"):
			for child in item.GetChildren():
				items.extend(getWidgets(child))
	return items
	
class MyApp(wx.App):
	def OnInit(self):
		self.frame = TFrame(None, wx.ID_ANY, "")
		self.SetTopWindow(self.frame)
		self.frame.Show()
		return True

if __name__ == "__main__":
	gettext.install("app") # replace with the appropriate catalog name
	app = MyApp(0)
	app.MainLoop()