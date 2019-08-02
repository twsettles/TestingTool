from testing_GUI import TestingFrame
import intake
from database import IssueDatabase
import wx, pickle, gettext, json, os
from tinydb import Query, where

COLOR ={"light":{"fg":"#000000", 'bg':'#ffffff'}, \
		'dark':{"fg":"#ffffff", 'bg':'#080808'}}

class TFrame(TestingFrame):
	ISSUE_SUMMARY = "Issue Summary"
	ISSUE_DESCRIPTION = "Issue Description"
	STEPS = "Steps to Reproduce"
	REMEDIATTION = "Remediation"
	SEVERITY = "Severity"
	USER_TYPE = intake.USER_TYPE
	PLATFORM = intake.PLATFORM
	CATEGORY = intake.CATEGORY
	BEST_PRACTICE = intake.BEST_PRACTICE
	WCAG = intake.WCAG
	
	def __init__(self, *args, **kwds):
		import glob
		TestingFrame.__init__(self,*args, **kwds)
		uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])
		self.settings = {}
		self.dark = False
		
		self.settings_file = 'settings.txt'
		self.dbfile = ''
		self.db = None
		self.load_db()
		
		#self.load_settings()
		self.Issue = Query()
		
		self.search_dict = \
		{intake.USER_TYPE: self.choice_user,
		intake.CATEGORY: self.choice_component,
		intake.BEST_PRACTICE: self.choice_best_practice,
		intake.PLATFORM: self.choice_platform,
		intake.WCAG: self.choice_wcag}
		
		for label, choice in self.search_dict.items():
			list_items = self.db.get_column_names(label)
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
		self.name = " - TTT"
		self.setTitle("Untitled")
		
		#Fields that are requiree/important
		self.important = {\
		TFrame.USER_TYPE: self.choice_user,
		TFrame.PLATFORM: self.choice_platform,
		TFrame.ISSUE_SUMMARY: self.text_ctrl_issue_summary,
		TFrame.ISSUE_DESCRIPTION: self.text_ctrl_issue_description,
		TFrame.STEPS: self.text_ctrl_steps_to_reproduce,
		TFrame.REMEDIATTION: self.text_ctrl_remediation,
		TFrame.SEVERITY: self.choice_severity,
		TFrame.CATEGORY: self.choice_component,
		TFrame.BEST_PRACTICE: self.choice_best_practice,
		TFrame.WCAG: self.choice_wcag}
		
		#sample info added to the tree
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
		#clear all selections 
		#TODO still needs to reset choices
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
		#TODO, update to not pickle the data
		self.setDirty(False)
		pickle.dump(self.data, file, pickle.HIGHEST_PROTOCOL)
		
	def on_menu_import(self, event):  # wxGlade: TestingFrame.<event_handler>
		"""
		Called when importing a report. Possibly used by managers (not implemented)
		"""
		#TODO, is this neccessary?
		print("Event handler 'on_menu_import' not implemented!")
		event.Skip()

	def on_menu_export_pdf(self, event):  # wxGlade: TestingFrame.<event_handler>
		"""
		Generates a word doc to be used for a PDF output
		"""
		#TODO, need to determine the format
		print("Event handler 'on_menu_export_pdf' not implemented!")
		event.Skip()

	def on_menu_export_excel(self, event):  # wxGlade: TestingFrame.<event_handler>
		"""
		Generates an excel doc of all issues.  possibly used to upload to JIRA
		"""
		#TODO, need to determine the format
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
		#TODO, need to refine this, so that users can save this setting
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
		#self.update_search()
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
		self.update_wcag_link()
		event.Skip()
			
	def on_text_issue_summary(self, event):
		self.setDirty(True)
		event.Skip()
		
	def safeToQuit(self):
		"""
		determines if there is unsaved work or if the user is ok with trashing changes
		"""
		if self.isDirty:
			return (wx.MessageBox("You have unsaved work. Are you sure you want to exit?", "Really exit?", wx.ICON_QUESTION | wx.YES_NO, self) == wx.YES)
		else:
			return True
	
	def on_notebook_page_changed(self, event):  # wxGlade: TestingFrame.<event_handler>
		#Data tab
		if event.GetSelection() == 4:
			self.text_ctrl_data.ChangeValue(str(self.data.__dict__))
		elif event.GetSelection() == 1:
			#update teh count box
			result = self.do_search()
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
	
	def on_button_submit(self, event):  # wxGlade: TestingFrame.<event_handler>
		#TODO - need to validate there is only one issue, based on filter, and save info to a new database
		data_to_save = dict()
		data_to_search = dict()
		done = True #False if there are empty fields
		to_finish = [] #array to keep track of unfnished fields
		for key, item in self.important.items():
			if type(item) == type(wx.TextCtrl()):
				data_to_save[key] = item.GetValue()
				
			elif type(item) == type(wx.Choice()):
				data_to_save[key] = self.get_choice_string(item)
			else:
				print(key)
			if data_to_save[key] in ('','All'):
				done = False
				to_finish.append(key)
		#test if ready to submit
		if not done:
			#pop alert
			message = "These fields aren't filled in\n"
			message += '\n'.join(to_finish)
			message += '\n\nContinue anyway?'
			continu = (wx.MessageBox(message, "You Fool!", wx.ICON_QUESTION | wx.CANCEL | wx.CANCEL_DEFAULT, self) == wx.OK)
			if not continu:
				return
			for k in to_finish:
				print(k)
		#build the search terms
		result = self.do_search()
		for elem in result:
			print(elem[intake.ISSUE_ID])
		#add issue to database
		#TODO
		#clear the fields on the second tab
		for field_name, field in self.important.items():
			if type(field) == type(wx.Choice()):
				pass
			elif type(field) == type(wx.TextCtrl()):
				field.SetValue('')
		event.Skip()
		
	def on_button_edit_issue(self, event):
		print("TBI - Edit")
		event.Skip()
		
	def on_button_delete_issue(self, event):
		print("TBI - Delete")
		event.Skip()
		
	def on_cell_select(self, event):
		print("{} {}".format(event.GetRow(), event.GetCol()))
		#controller = event.GetEventObject()
		self.Bind(wx.EVT_KEY_DOWN, self.on_cell_key_down)
		event.Skip()
	
	def on_cell_key_down(self,event):
		keycode = event.GetKeyCode()
		#print(keycode)
		for key in dir(wx.KeyCode):
			if key == 307: #application key
				print(key)
		event.Skip()
	
	def do_search(self):
		'''
		Performs a search based on the current selection of the wxChoices
		'''
		dd = dict()
		for k, v in self.search_dict.items():
			selection = self.get_choice_string(v)
			if not selection == "All":
				dd[k] = selection
		return self.db.compound_search(dd)
	
	def update_wcag_link(self):
		"""
		Updates the WCAG link field, based on the WCAG criteria choice
		"""
		selection = self.get_choice_string(self.choice_wcag)
		if selection == "All":
			self.text_ctrl_wcag.SetValue("")
		results = self.db.search(self.Issue[intake.WCAG] == selection)
		if len(results):
			self.text_ctrl_wcag.SetValue(results[0][intake.LINK])
		
	def update_search(self):
		"""
		Generic function that calculates and updates the choices in a wxChoice
		Called by all of the wxChoices that can change search results
		"""
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
			results = self.db.compound_search(copy_string_dict)
			#print("len(results):\t"+str(len(results)))
			list_to_append = []
			#print("results[0]:\t" + str(results[0]))
			#print("string:\t"+ string)
			for item in results:
				#print(item[k])
				list_to_append.append(item[string])
			list_to_append = list(set(list_to_append))
			self.reset_choices(choice,list_to_append)
		self.update_wcag_link()
		result = self.do_search()
		count = len(result)
		self.text_ctrl_count.ChangeValue(str(count))
		
	def get_choice_string(self,choice):
		"""
		Given a wxChoice, returns its selected string
		"""
		selection_int = choice.GetSelection()
		return choice.GetString(selection_int)
		
	def reset_choices(self,choice, choices):
		"""
		Given a list of choices, and a wxChoice, it sets the choicse to the list
		and retains the previous selection
		"""
		current = self.get_choice_string(choice)
		choice.Clear()
		choice.AppendItems(["All"])
		choices = list(set(choices))
		choices.sort()
		choice.AppendItems(choices)
		''' removed because it can trap the user if two fields are pigeon-holed
		if len(choices) == 1:
			sel_int = 1
		else:
		'''
		sel_int = choice.FindString(current)
		choice.SetSelection(sel_int)
	
	def load_db(self):
		try:
			self.db = IssueDatabase('db.json')
		except:
			try:
				path = self.get_file_path("Open the issues database file", 'json')
				self.db = IssueDatabase(path)
			except:
				print("everything broke")
	
	def load_settings(self): #TODO
		"""
		Load settings from "settings.txt"
		# Not working correctly
		"""
		try:
			f = open(self.settings_file, 'rt')
			string = f.read()
		except IOError:
			settings = self.get_file_path('Open the settings file', 'txt')
			f = open(settings, 'wt')
			string = '{"dark": False, "dbfile":'+self.dbfile + '}'
		finally:
			if string:
				try:
					settings_handler = eval(string)
					if not type(settings_handler) == type(dict()):
						raise KeyError
				except:
					settings_handler = {'dark': False, "dbfile":"db.json"}
			else:
				settings_handler = {'dark': False, "dbfile":"db.json"}
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
			
			#save the settings for next time
			string = str({'dark': self.dark, 'dbfile': self.dbfile})
			if not 'w' in f.mode:
				f.close()
				f = open(settings_file, 'wt')
			f.write(string)
			f.close()

	def get_file_path(self, mess: str, ext: str):
		wc_str = ext.upper() + ' Files (*.' + ext + ')|*.' + ext
		with wx.FileDialog(self, message = mess, wildcard=wc_str, style=wx.FD_OPEN |wx.FD_FILE_MUST_EXIST) as dlg:
				if dlg.ShowModal() == wx.ID_OK:
					return dlg.GetPath()
				return "Nah"
		return "Nope"

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
