#!/usr/bin/env python
# -*- coding: ISO-8859-15 -*-
#
# generated by wxGlade 0.9.3 on Wed Aug 14 10:28:02 2019
#

import wx
import wx.grid

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class TestingFrame(wx.Frame):
	def __init__(self, *args, **kwds):
		# begin wxGlade: TestingFrame.__init__
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)
		self.SetSize((856, 549))
		
		# Menu Bar
		self.frame_menubar = wx.MenuBar()
		wxglade_tmp_menu = wx.Menu()
		self.frame_menubar.file_new = wxglade_tmp_menu.Append(wx.ID_NEW, "&New\tCtrl-N", "Create a New Report")
		self.Bind(wx.EVT_MENU, self.on_menu_new, id=wx.ID_NEW)
		wxglade_tmp_menu.Append(wx.ID_OPEN, "&Open\tCtrl-O", "Open a Saved File")
		self.Bind(wx.EVT_MENU, self.on_menu_open, id=wx.ID_OPEN)
		wxglade_tmp_menu.Append(wx.ID_SAVE, "&Save\tCtrl-S", "Save your work!")
		self.Bind(wx.EVT_MENU, self.on_menu_save, id=wx.ID_SAVE)
		wxglade_tmp_menu.Append(wx.ID_SAVEAS, "Save As\tCtrl-Shift-S", "")
		self.Bind(wx.EVT_MENU, self.on_menu_save_as, id=wx.ID_SAVEAS)
		wxglade_tmp_menu.AppendSeparator()
		item = wxglade_tmp_menu.Append(wx.ID_ANY, "&Import\tCtrl-I", "Import issues from an Excel doc")
		self.Bind(wx.EVT_MENU, self.on_menu_import, id=item.GetId())
		wxglade_tmp_menu_sub = wx.Menu()
		item = wxglade_tmp_menu_sub.Append(wx.ID_ANY, "&PDF\tCtrl-P", "Generate a pretty PDF")
		self.Bind(wx.EVT_MENU, self.on_menu_export_pdf, id=item.GetId())
		item = wxglade_tmp_menu_sub.Append(wx.ID_ANY, "&Excel\tCtrl-E", "Generate a an Excel doc")
		self.Bind(wx.EVT_MENU, self.on_menu_export_excel, id=item.GetId())
		wxglade_tmp_menu.Append(wx.ID_ANY, "&Export", wxglade_tmp_menu_sub, "")
		wxglade_tmp_menu.AppendSeparator()
		wxglade_tmp_menu.Append(wx.ID_EXIT, "E&xit\tALT-F4", "Close the Application")
		self.Bind(wx.EVT_MENU, self.on_menu_exit, id=wx.ID_EXIT)
		self.frame_menubar.Append(wxglade_tmp_menu, "&File")
		wxglade_tmp_menu = wx.Menu()
		item = wxglade_tmp_menu.Append(wx.ID_ANY, "Dark Mode", "Toggle Dark Mode (experimental)", wx.ITEM_CHECK)
		self.Bind(wx.EVT_MENU, self.on_menu_dark, id=item.GetId())
		self.frame_menubar.Append(wxglade_tmp_menu, "View")
		wxglade_tmp_menu = wx.Menu()
		wxglade_tmp_menu.Append(wx.ID_ABOUT, "&About\tCtrl-H", "Information on the Apllication")
		self.Bind(wx.EVT_MENU, self.on_menu_about, id=wx.ID_ABOUT)
		self.frame_menubar.Append(wxglade_tmp_menu, "Help")
		self.SetMenuBar(self.frame_menubar)
		# Menu Bar end
		self.notebook_1 = wx.Notebook(self, wx.ID_ANY)
		self.notebook_1_pane_2 = wx.Panel(self.notebook_1, wx.ID_ANY)
		self.choice_platform = wx.Choice(self.notebook_1_pane_2, wx.ID_ANY, choices=["All"])
		self.choice_user = wx.Choice(self.notebook_1_pane_2, wx.ID_ANY, choices=["All"])
		self.notebook_1_pane_3 = wx.Panel(self.notebook_1, wx.ID_ANY)
		self.text_ctrl_issue_summary = wx.TextCtrl(self.notebook_1_pane_3, wx.ID_ANY, "")
		self.text_ctrl_issue_description = wx.TextCtrl(self.notebook_1_pane_3, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
		self.text_ctrl_steps_to_reproduce = wx.TextCtrl(self.notebook_1_pane_3, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
		self.text_ctrl_remediation = wx.TextCtrl(self.notebook_1_pane_3, wx.ID_ANY, "", style=wx.TE_MULTILINE)
		self.choice_severity = wx.Choice(self.notebook_1_pane_3, wx.ID_ANY, choices=["P1", "P2", "P3"])
		self.choice_component = wx.Choice(self.notebook_1_pane_3, wx.ID_ANY, choices=["All"])
		self.choice_best_practice = wx.Choice(self.notebook_1_pane_3, wx.ID_ANY, choices=["All"])
		self.choice_wcag = wx.Choice(self.notebook_1_pane_3, wx.ID_ANY, choices=["All"])
		self.text_ctrl_wcag = wx.TextCtrl(self.notebook_1_pane_3, wx.ID_ANY, "", style=wx.TE_AUTO_URL | wx.TE_DONTWRAP | wx.TE_MULTILINE | wx.TE_NO_VSCROLL | wx.TE_READONLY)
		self.button_submit = wx.Button(self.notebook_1_pane_3, wx.ID_ANY, "Submit")
		self.text_ctrl_count = wx.TextCtrl(self.notebook_1_pane_3, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY)
		self.notebook_1_LoggedIssues = wx.Panel(self.notebook_1, wx.ID_ANY)
		self.tree_ctrl_1 = wx.TreeCtrl(self.notebook_1_LoggedIssues, wx.ID_ANY, style=wx.TR_DEFAULT_STYLE | wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT | wx.TR_TWIST_BUTTONS)
		self.button_edit_2 = wx.Button(self.notebook_1_LoggedIssues, wx.ID_ANY, "Edit Issue")
		self.button_delete_2 = wx.Button(self.notebook_1_LoggedIssues, wx.ID_ANY, "Delete Issue")
		self.notebook_1_pane_table_ssiues = wx.Panel(self.notebook_1, wx.ID_ANY)
		self.grid_1 = wx.grid.Grid(self.notebook_1_pane_table_ssiues, wx.ID_ANY, size=(1, 1))
		self.grid_1.SetTabBehaviour(wx.grid.Grid.TabBehaviour.Tab_Leave)
		self.button_edit_1 = wx.Button(self.notebook_1_pane_table_ssiues, wx.ID_ANY, "Edit Issue")
		self.button_delete_1 = wx.Button(self.notebook_1_pane_table_ssiues, wx.ID_ANY, "Delete Issue")
		self.notebook_1_DataFrame = wx.Panel(self.notebook_1, wx.ID_ANY)
		self.text_ctrl_data = wx.TextCtrl(self.notebook_1_DataFrame, wx.ID_ANY, "")

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_CHOICE, self.on_choice_platform, self.choice_platform)
		self.Bind(wx.EVT_CHOICE, self.on_choice_user, self.choice_user)
		self.Bind(wx.EVT_TEXT, self.on_text_issue_summary, self.text_ctrl_issue_summary)
		self.Bind(wx.EVT_CHOICE, self.on_choice_priority, self.choice_severity)
		self.Bind(wx.EVT_CHOICE, self.on_choice_component, self.choice_component)
		self.Bind(wx.EVT_CHOICE, self.on_choice_best_preactice, self.choice_best_practice)
		self.Bind(wx.EVT_CHOICE, self.on_choice_wcag, self.choice_wcag)
		self.Bind(wx.EVT_BUTTON, self.on_button_submit, self.button_submit)
		self.Bind(wx.EVT_BUTTON, self.on_button_edit_issue, self.button_edit_2)
		self.Bind(wx.EVT_BUTTON, self.on_button_delete_issue, self.button_delete_2)
		self.Bind(wx.grid.EVT_GRID_CMD_SELECT_CELL, self.on_cell_select, self.grid_1)
		self.Bind(wx.EVT_BUTTON, self.on_button_edit_issue, self.button_edit_1)
		self.Bind(wx.EVT_BUTTON, self.on_button_delete_issue, self.button_delete_1)
		self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_notebook_page_changed, self.notebook_1)
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: TestingFrame.__set_properties
		self.SetTitle("frame")
		self.choice_platform.SetSelection(0)
		self.choice_user.SetSelection(0)
		self.choice_component.SetSelection(0)
		self.choice_best_practice.SetSelection(0)
		self.choice_wcag.SetSelection(0)
		self.grid_1.CreateGrid(10, 2)
		self.grid_1.EnableDragRowSize(0)
		self.grid_1.EnableDragGridSize(0)
		self.grid_1.SetColLabelValue(0, "Issue Description")
		self.grid_1.SetColLabelValue(1, "Severity")
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: TestingFrame.__do_layout
		sizer_1 = wx.BoxSizer(wx.VERTICAL)
		sizer_7 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_DataFrame, wx.ID_ANY, "Data"), wx.HORIZONTAL)
		sizer_20 = wx.BoxSizer(wx.VERTICAL)
		sizer_21 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_18 = wx.BoxSizer(wx.VERTICAL)
		sizer_22 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_5 = wx.FlexGridSizer(1, 2, 0, 12)
		sizer_6 = wx.BoxSizer(wx.VERTICAL)
		sizer_19 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, wx.ID_ANY, "Matching Issues"), wx.HORIZONTAL)
		sizer_8 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, wx.ID_ANY, "WCAG"), wx.VERTICAL)
		sizer_9 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, wx.ID_ANY, "Best Practice"), wx.VERTICAL)
		sizer_10 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, wx.ID_ANY, "Component Type"), wx.VERTICAL)
		sizer_12 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, wx.ID_ANY, "Severity"), wx.VERTICAL)
		sizer_11 = wx.BoxSizer(wx.VERTICAL)
		sizer_17 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, wx.ID_ANY, "Remediation"), wx.HORIZONTAL)
		sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_16 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, wx.ID_ANY, "Steps to Reproduce"), wx.HORIZONTAL)
		sizer_14 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, wx.ID_ANY, "Issue Description"), wx.HORIZONTAL)
		sizer_15 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_3, wx.ID_ANY, "Issue Summary"), wx.HORIZONTAL)
		sizer_2 = wx.BoxSizer(wx.VERTICAL)
		sizer_4 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_2, wx.ID_ANY, "User Type"), wx.VERTICAL)
		sizer_3 = wx.StaticBoxSizer(wx.StaticBox(self.notebook_1_pane_2, wx.ID_ANY, "Platform"), wx.HORIZONTAL)
		sizer_3.Add(self.choice_platform, 0, 0, 0)
		sizer_2.Add(sizer_3, 0, wx.ALL | wx.EXPAND, 2)
		sizer_4.Add(self.choice_user, 0, 0, 0)
		sizer_2.Add(sizer_4, 0, wx.EXPAND, 0)
		self.notebook_1_pane_2.SetSizer(sizer_2)
		sizer_15.Add(self.text_ctrl_issue_summary, 1, 0, 0)
		sizer_11.Add(sizer_15, 0, wx.ALL | wx.EXPAND | wx.FIXED_MINSIZE, 0)
		sizer_14.Add(self.text_ctrl_issue_description, 1, wx.EXPAND, 0)
		sizer_13.Add(sizer_14, 1, wx.EXPAND, 0)
		sizer_16.Add(self.text_ctrl_steps_to_reproduce, 1, wx.EXPAND, 0)
		sizer_13.Add(sizer_16, 1, wx.EXPAND, 0)
		sizer_11.Add(sizer_13, 1, wx.EXPAND, 0)
		sizer_17.Add(self.text_ctrl_remediation, 1, 0, 0)
		sizer_11.Add(sizer_17, 0, wx.EXPAND, 0)
		sizer_5.Add(sizer_11, 0, wx.EXPAND, 0)
		sizer_12.Add(self.choice_severity, 1, wx.EXPAND, 0)
		sizer_6.Add(sizer_12, 0, wx.EXPAND, 0)
		sizer_10.Add(self.choice_component, 1, wx.EXPAND, 0)
		sizer_6.Add(sizer_10, 0, wx.EXPAND, 0)
		sizer_9.Add(self.choice_best_practice, 1, wx.EXPAND, 0)
		sizer_6.Add(sizer_9, 0, wx.EXPAND, 0)
		sizer_8.Add(self.choice_wcag, 0, wx.EXPAND, 0)
		sizer_8.Add(self.text_ctrl_wcag, 0, wx.EXPAND | wx.FIXED_MINSIZE, 0)
		sizer_6.Add(sizer_8, 0, wx.EXPAND, 0)
		sizer_6.Add(self.button_submit, 0, 0, 0)
		sizer_19.Add(self.text_ctrl_count, 0, 0, 0)
		sizer_6.Add(sizer_19, 1, wx.EXPAND, 0)
		sizer_5.Add(sizer_6, 0, 0, 0)
		self.notebook_1_pane_3.SetSizer(sizer_5)
		sizer_5.AddGrowableRow(0)
		sizer_5.AddGrowableCol(0)
		sizer_18.Add(self.tree_ctrl_1, 1, wx.EXPAND, 0)
		sizer_22.Add(self.button_edit_2, 0, 0, 0)
		sizer_22.Add(self.button_delete_2, 0, 0, 0)
		sizer_18.Add(sizer_22, 1, wx.EXPAND, 0)
		self.notebook_1_LoggedIssues.SetSizer(sizer_18)
		sizer_20.Add(self.grid_1, 1, wx.ALL | wx.EXPAND, 1)
		sizer_21.Add(self.button_edit_1, 0, 0, 0)
		sizer_21.Add(self.button_delete_1, 0, 0, 0)
		sizer_20.Add(sizer_21, 1, wx.EXPAND, 0)
		self.notebook_1_pane_table_ssiues.SetSizer(sizer_20)
		sizer_7.Add(self.text_ctrl_data, 1, wx.ALL | wx.EXPAND, 0)
		self.notebook_1_DataFrame.SetSizer(sizer_7)
		self.notebook_1.AddPage(self.notebook_1_pane_2, "Global Settings")
		self.notebook_1.AddPage(self.notebook_1_pane_3, "Create an Issue")
		self.notebook_1.AddPage(self.notebook_1_LoggedIssues, "Logged Issues")
		self.notebook_1.AddPage(self.notebook_1_pane_table_ssiues, "Logged Issues")
		self.notebook_1.AddPage(self.notebook_1_DataFrame, "Data Frame")
		sizer_1.Add(self.notebook_1, 1, wx.ALL | wx.EXPAND, 5)
		self.SetSizer(sizer_1)
		self.Layout()
		# end wxGlade

	def on_menu_new(self, event):  # wxGlade: TestingFrame.<event_handler>
		print("Event handler 'on_menu_new' not implemented!")
		event.Skip()

	def on_menu_open(self, event):  # wxGlade: TestingFrame.<event_handler>
		print("Event handler 'on_menu_open' not implemented!")
		event.Skip()

	def on_menu_save(self, event):  # wxGlade: TestingFrame.<event_handler>
		print("Event handler 'on_menu_save' not implemented!")
		event.Skip()

	def on_menu_save_as(self, event):  # wxGlade: TestingFrame.<event_handler>
		print("Event handler 'on_menu_save_as' not implemented!")
		event.Skip()

	def on_menu_import(self, event):  # wxGlade: TestingFrame.<event_handler>
		print("Event handler 'on_menu_import' not implemented!")
		event.Skip()

	def on_menu_export_pdf(self, event):  # wxGlade: TestingFrame.<event_handler>
		print("Event handler 'on_menu_export_pdf' not implemented!")
		event.Skip()

	def on_menu_export_excel(self, event):  # wxGlade: TestingFrame.<event_handler>
		print("Event handler 'on_menu_export_excel' not implemented!")
		event.Skip()

	def on_menu_exit(self, event):  # wxGlade: TestingFrame.<event_handler>
		print("Event handler 'on_menu_exit' not implemented!")
		event.Skip()

	def on_menu_dark(self, event):  # wxGlade: TestingFrame.<event_handler>
		print("Event handler 'on_menu_dark' not implemented!")
		event.Skip()

	def on_menu_about(self, event):  # wxGlade: TestingFrame.<event_handler>
		print("Event handler 'on_menu_about' not implemented!")
		event.Skip()

	def on_choice_platform(self, event):  # wxGlade: TestingFrame.<event_handler>
		print("Event handler 'on_choice_platform' not implemented!")
		event.Skip()

	def on_choice_user(self, event):  # wxGlade: TestingFrame.<event_handler>
		print("Event handler 'on_choice_user' not implemented!")
		event.Skip()

	def on_text_issue_summary(self, event):  # wxGlade: TestingFrame.<event_handler>
		print("Event handler 'on_text_issue_summary' not implemented!")
		event.Skip()

	def on_choice_priority(self, event):  # wxGlade: TestingFrame.<event_handler>
		print("Event handler 'on_choice_priority' not implemented!")
		event.Skip()

	def on_choice_component(self, event):  # wxGlade: TestingFrame.<event_handler>
		print("Event handler 'on_choice_component' not implemented!")
		event.Skip()

	def on_choice_best_preactice(self, event):  # wxGlade: TestingFrame.<event_handler>
		print("Event handler 'on_choice_best_preactice' not implemented!")
		event.Skip()

	def on_choice_wcag(self, event):  # wxGlade: TestingFrame.<event_handler>
		print("Event handler 'on_choice_wcag' not implemented!")
		event.Skip()

	def on_button_submit(self, event):  # wxGlade: TestingFrame.<event_handler>
		print("Event handler 'on_button_submit' not implemented!")
		event.Skip()

	def on_button_edit_issue(self, event):  # wxGlade: TestingFrame.<event_handler>
		print("Event handler 'on_button_edit_issue' not implemented!")
		event.Skip()

	def on_button_delete_issue(self, event):  # wxGlade: TestingFrame.<event_handler>
		print("Event handler 'on_button_delete_issue' not implemented!")
		event.Skip()

	def on_cell_select(self, event):  # wxGlade: TestingFrame.<event_handler>
		print("Event handler 'on_cell_select' not implemented!")
		event.Skip()

	def on_notebook_page_changed(self, event):  # wxGlade: TestingFrame.<event_handler>
		print("Event handler 'on_notebook_page_changed' not implemented!")
		event.Skip()

# end of class TestingFrame

class MyApp(wx.App):
	def OnInit(self):
		self.frame = TestingFrame(None, wx.ID_ANY, "")
		self.SetTopWindow(self.frame)
		self.frame.Show()
		return True

# end of class MyApp

if __name__ == "__main__":
	app = MyApp(0)
	app.MainLoop()
