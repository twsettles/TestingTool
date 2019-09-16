from testing_GUI import TestingFrame
import tool
import File_opener as FO
import wx, os, sys
from typing import Optional, List, Dict, IO, Iterable

class TFrame(TestingFrame):
	def __init__(self, *args, **kwds) -> None:
		TestingFrame.__init__(self,*args, **kwds)
		self.dark: bool = False
		self.pathname:str = ''
		self.hub = tool.Hub() #interacts with all other modules
		self.f_dlg = FO.FileDialog()
		
		self.search_dict = {
		tool.USER_TYPE: self.choice_user,
		tool.CATEGORY: self.choice_component,
		tool.BEST_PRACTICE: self.choice_best_practice,
		tool.PLATFORM: self.choice_platform,
		tool.WCAG: self.choice_wcag}
		
		#Fields that are requiree/important
		self.important = {
		tool.USER_TYPE: self.choice_user,
		tool.PLATFORM: self.choice_platform,
		tool.ISSUE_SUMMARY: self.text_ctrl_issue_summary,
		tool.STEPS: self.text_ctrl_steps_to_reproduce,
		tool.ISSUE_DESCRIPTION: self.text_ctrl_issue_description,
		tool.SEVERITY: self.choice_severity,
		tool.REMEDIATTION: self.text_ctrl_remediation,
		tool.CATEGORY: self.choice_component,
		tool.BEST_PRACTICE: self.choice_best_practice,
		tool.WCAG: self.choice_wcag}
		
		#sample info added to the tree
		self.root = self.tree_ctrl_1.AddRoot("All Issues")
		self.tree_issues: Dict = {}
		
		self.populate_wx_choices()
		self.set_title()
		
	def populate_wx_choices(self) -> None:
		"""populates all the choices as if the user just opened the program"""
		for label, choice in self.search_dict.items():
			list_items = self.hub.get_possible(label)
			set_choice(choice, list_items)			
	
	def set_dirty(self, isDirty: bool) -> None:
		"""Marks the current work as different/same from the saved file"""
		self.hub.set_dirty(isDirty)
		self.set_title()
		
	def set_title(self) -> None:
		"""Sets the title of the window to the file pathname"""
		self.SetTitle(self.hub.get_title())
	
	def on_menu_new(self, event: 'wx.Event') -> None: 
		"""Called on file>new or ctrl+n"""
		override = self.safeToQuit()
		if self.hub.clear_issue_l(override):
			self.tree_ctrl_1.DeleteChildren(self.root)
			self.hub.set_title('new') 
			self.populate_wx_choices()
			self.hub.set_curr_issue_id(-1)
			self.hub.set_notes('')
			self.text_ctrl_notes.SetValue(self.hub.get_notes())
			self.set_dirty(False)
	
	def on_menu_open(self, event: 'wx.Event') -> None:
		"""Called on file>open or ctrl+o"""
		if not self.safeToQuit():
			return
		
		filename = self.f_dlg.get_path(mode = 'Open', wc = FO.RPT_WC)
		
		if filename:
			self.pathname = filename
			with open(filename,'r') as f:
				self.on_menu_new(event)
				self.hub.replace_issue_list(f)
				f.close()
				self.hub.set_title(get_name_from_file(filename))
				self.set_title()
				self.hub.set_curr_issue_id(-1)
				self.text_ctrl_notes.SetValue(self.hub.get_notes())
				platform = self.hub.get_platform()
				if platform:
					set_chocie_or_text(self.important[tool.PLATFORM],platform)
				self.set_dirty(False)
		else:
			print("No file selected")
	
	def on_menu_save(self, event: 'wx.Event') -> None:  # wxGlade: TestingFrame.<event_handler>
		"""Called on file>save or ctrl+s"""
		if self.pathname:
			self.save_as(self.pathname)
		else:
			self.on_menu_save_as(event)
	
	def on_menu_save_as(self, event: 'wx.Event') -> None:
		"""Called on file>save_as or ctrl+shift+s"""
		# save the current contents in the file
		try:
			pathname = self.f_dlg.get_path(mode='Save', wc = FO.RPT_WC)
			self.save_as(pathname)
		except Exception as e: print(e)
	
	def save_as(self, pathname: str) -> None:
		"""does the work for both on_menu_save_as and on_menu_save"""
		with open(pathname, 'w') as file:
			self.hub.set_title(get_name_from_file(pathname))
			self.hub.set_notes(self.text_ctrl_notes.GetValue())
			self.set_title()
			self.pathname = pathname
			self.doSaveData(file)
			file.close()
	
	def doSaveData(self, file: IO[str]) -> None:
		"""Does the actual work of saving"""
		self.set_dirty(False)
		self.hub.write_issues(file)
	
	def on_menu_import(self, event):  # wxGlade: TestingFrame.<event_handler>
		"""Called when importing a report. Possibly used by managers (not implemented)"""
		#TODO, is this neccessary?
		print("Event handler 'on_menu_import' not implemented!")
		event.Skip()
	
	def on_menu_export_pdf(self, event):  # wxGlade: TestingFrame.<event_handler>
		"""Generates a word doc to be used for a PDF output"""
		#TODO, need to determine the format
		print("Event handler 'on_menu_export_pdf' not implemented!")
		event.Skip()
	
	def on_menu_export_excel(self, event):  # wxGlade: TestingFrame.<event_handler>
		"""Generates an excel doc of all issues.  possibly used to upload to JIRA"""
		self.hub.generate_report()
		event.Skip()
	
	def on_menu_exit(self, event):
		"""Called on file>exit or alt+f4"""
		if self.safeToQuit():
			self.f_dlg.tear_down()
			self.Close()
		else:
			event.StopPropagation()
	
	def on_menu_about(self, event):
		"""Used to learn about the program e.g. version number..."""
		#TODO
		event.Skip()
	
	def on_menu_dark(self, event):
		"""Used to turn on/off dark mode"""
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
	
	def on_choice_platform(self, event): 
		self.on_generic(event)
	
	def on_choice_user(self, event):  # wxGlade: TestingFrame.<event_handler>
		self.on_generic(event)
	
	def on_choice_priority(self, event):  # wxGlade: TestingFrame.<event_handler>
		self.on_generic(event, False)
	
	def on_choice_component(self, event):  # wxGlade: TestingFrame.<event_handler>
		self.on_generic(event)
	
	def on_choice_best_preactice(self, event):  # wxGlade: TestingFrame.<event_handler>	
		self.on_generic(event)
	
	def on_choice_wcag(self, event):  # wxGlade: TestingFrame.<event_handler>
		self.on_generic(event)
		self.update_wcag_link()
	
	def on_text_issue_summary(self, event):
		self.on_generic(event, False)
		
	def on_text_notes(self, event):
		self.on_generic(event, False)
	
	def safeToQuit(self):
		"""determines if there is unsaved work or if the user is ok with trashing changes"""
		if self.hub.get_dirty():
			answer = wx.MessageDialog(self,
			"You have unsaved work. Are you sure you want to continue?",
			"Are you sure?", 
			wx.ICON_QUESTION | wx.YES_NO
			).ShowModal()
			return answer == wx.ID_YES
		else:
			return True
	
	def on_notebook_page_changed(self, event):  # wxGlade: TestingFrame.<event_handler>
		if event.GetSelection() == 3: # raw data tab
			self.raw_data_tab_selected(event)
		elif event.GetSelection() == 1: # per issue tab
			self.create_issue_tab_selected(event)
		elif event.GetSelection() == 2: # tree Issue tab
			self.tree_tab_selected(event)
	
	def raw_data_tab_selected(self, event):
		import json
		to_place:str = json.dumps(
		self.hub.get_issues().__dict__,
		indent = 4,)
		to_place += '\nDirty: ' + str(self.hub.get_dirty())
		self.text_ctrl_data.ChangeValue(to_place)

	def create_issue_tab_selected(self, event):
		"""updates the count box"""
		result = self.do_search()
		count = len(result)
		self.text_ctrl_count.ChangeValue(str(count))
	
	def tree_tab_selected(self, event):
		self.tree_ctrl_1.DeleteChildren(self.root)
		for i, item in enumerate(self.hub.get_issues()):
			summ = item[tool.ISSUE_SUMMARY]
			self.tree_issues[self.tree_ctrl_1.AppendItem(self.root, summ)] = item[tool.NUM]
	
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
				data_to_save[key] = get_choice_string(item)
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
			print(elem[tool.ISSUE_ID])
		#add issue to database
		if self.hub.get_curr_issue_id() == -1:
			self.hub.add_issue(data_to_save)
		else:
			self.hub.update_issue(data_to_save)
			self.hub.set_curr_issue_id(-1)
		#clear the fields on the second tab
		for field in getWidgets(self.notebook_1_pane_3):
			if not (field == self.choice_severity):
				clear_input(field)
		self.populate_wx_choices()
		self.update_search()
		event.Skip()
		
	def on_button_edit_issue(self, event):
		try:
			issue_id = self.get_tree_selected_isssue()
			self.notebook_1.ChangeSelection(1) #move focus to the "create issue" tab
			issue = self.hub.get_issue(issue_id)
			for field, entry in issue.items():
				if field in self.important.keys():
					set_chocie_or_text(self.important[field], entry)
			self.update_search()
			self.hub.set_curr_issue_id(issue_id)
		except TypeError:
			pass #TODO add dialog
		event.Skip()
		
	def on_button_delete_issue(self, event):
		try:
			issue_id = self.get_tree_selected_isssue()
			print(issue_id)
			self.hub.remove_issue(issue_id)
			self.tree_tab_selected(event)
		except TypeError:
			pass #TODO add dialog
		event.Skip()
	
	def do_search(self):
		'''Performs a search based on the current selection of the wxChoices'''
		dd: Dict[str, str] = {}
		for k, v in self.search_dict.items():
			selection = get_choice_string(v)
			if not selection == "All":
				dd[k] = selection
		return self.hub.compound_search(dd)
	
	def update_wcag_link(self):
		link = self.hub.get_wcag_link(get_choice_string(self.choice_wcag))
		self.text_ctrl_wcag.SetValue(link)
		
	def update_search(self):
		"""
		Generic function that calculates and updates the choices in a wxChoice
		Called by all of the wxChoices that can change search results
		"""
		for string, choice in self.search_dict.items():
			#remove the current option from the dict for the search
			copy_string_dict: Dict = {}
			for k,v in self.search_dict.items():
				if k == string:
					continue
				if not "All" == get_choice_string(v):
					copy_string_dict[k] = get_choice_string(v)
			results: List = self.hub.compound_search(copy_string_dict)
			list_to_append:List = []
			for item in results:
				list_to_append.append(item[string])
			list_to_append = list(set(list_to_append))
			set_choice(choice,list_to_append)
		self.update_wcag_link()
		count = len(self.do_search())
		self.text_ctrl_count.ChangeValue(str(count))
		
	def get_tree_selected_isssue(self) -> int:
		selection = self.tree_ctrl_1.GetSelection()
		return self.tree_issues[selection]
	
	def clear_inputs(self) -> None:
		for field, entry in self.important.items():
			clear_input(entry)

	def on_generic(self, event, update:bool = True) -> None:
		print(event.__dict__)
		if update: self.update_search()
		self.set_dirty(True)
		event.Skip()
			
def set_choice(choice: 'wx.Choice', options: List[str]) -> None:
	curr_sel = get_choice_string(choice)
	clear_input(choice)
	choice.AppendItems(['All'])
	options.sort()
	choice.AppendItems(options)
	sel_int = choice.FindString(curr_sel)
	choice.SetSelection(sel_int)

def get_choice_string(choice: 'wx.Choice') -> str:
	"""
	Given a wxChoice, returns its selected string
	"""
	selection_int = choice.GetSelection()
	return choice.GetString(selection_int)

def clear_input(entry):
	if isinstance(entry,wx.Choice):
		entry.Clear()
	elif isinstance(entry, wx.TextCtrl):
		entry.SetValue('')
			
def set_chocie_or_text(control, value):
	if isinstance(control, wx.TextCtrl):
		control.SetValue(value)
	elif isinstance(control, wx.Choice):	
		sel_int = control.FindString(value)
		if sel_int == -1:
			control.AppendItems([value])
			sel_int = control.FindString(value)
		control.SetSelection(sel_int)

def get_name_from_file(file_name: str) -> str:
	"""
	Given a full file path C:/one/foo.rpt returns foo
	Used to get the title of the window
	"""
	broken_file: List = file_name.split(os.sep)
	return (broken_file[-1][:-4])

def getWidgets(parent) -> List:
	"""Return a list of all the child widgets"""
	items = [parent]
	for item in parent.GetChildren():
		items.append(item)
		if hasattr(item, "GetChildren"):
			for child in item.GetChildren():
				items.extend(getWidgets(child))
	return items
		
class MyApp(wx.App):
	def OnInit(self) -> bool:
		self.frame = TFrame(None, wx.ID_ANY, "")
		self.frame.Show()
		return True

if __name__ == "__main__":
	app = MyApp(0)
	app.MainLoop()
