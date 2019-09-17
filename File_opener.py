import wx

JSON_WC = "JSON Files (*.json)|*.json"
RPT_WC = "RPT Files (*.rpt)|*.rpt"
PY_WC = "Python Files (*.py)|*.py"
XLS_WC = "Excel Files (*.xls)|*.xls"
ALL_WC = "All Files (*.*)|*.*"

class FileDialog():
	def __init__(self, parent):
		self.parent = parent
		self.frame = wx.Frame(parent,wx.ID_ANY,'')
	
	def tear_down(self):
		self.frame.Close()
	
	def get_path(self, mode: str = '', msg: str = '', wc: str = ALL_WC) -> str:
		if mode == 'Open':
			if not msg:
				msg = "Open a file"
			arg = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
		elif mode == 'Save':
			if not msg:
				msg = "Save a file"
			arg = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
		elif mode == 'New':
			if not msg:
				msg = "Create a File"
			arg = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
		else:
			msg = 'Malfomred mode'
			arg = wx.FD_DEFAULT_STYLE
		
		dialog = wx.FileDialog(self.parent, msg, '', '', wc, arg)
		dialog.ShowModal()
		path = dialog.GetPath()
		return path
		
	
		
def main() -> None:
	class MyApp(wx.App):
		def OnInit(self):
			self.frame = wx.Frame(None,wx.ID_ANY, '')
			self.frame.Show()
			return True
	app = MyApp(0)
	print((FileDialog(app.frame)).get_path(mode = 'Save', wc = PY_WC))
		
if __name__ == '__main__':
	main()