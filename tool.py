import File_opener as FO
import intake
import export
from database import IssueDatabase
from issue_list import IssueList
import wx, gettext, json, os
from typing import Optional, List, Dict, IO

ISSUE_SUMMARY = "Issue Summary"
ISSUE_DESCRIPTION = "Issue Description"
STEPS = "Steps to Reproduce"
REMEDIATTION = "Remediation"
SEVERITY = "Severity"
USER_TYPE = intake.USER_TYPE
CATEGORY = intake.CATEGORY
BEST_PRACTICE = intake.BEST_PRACTICE
PLATFORM = intake.PLATFORM
WCAG = intake.WCAG
ISSUE_ID = intake.ISSUE_ID
NUM = IssueList.NUM


class Hub:
	def __init__(self) -> None:
		self.db = IssueDatabase()
		self.issue_l = IssueList()
		self.curr_issue_id = -1
		self.dirty: bool = False
		self.title:str = 'new'
		self.title_suffix: str = ' - TTT'
		
		self.load_db()
	
	def load_db(self) -> None:
		try:
			self.db = IssueDatabase('db.json')
		except:
			try:
				self.db = IssueDatabase(r'C:\Users\p2763554\Documents\GitHub\TestingTool\db.json')
			except:
				try:
					dlg = FO.FileDialog()
					path = dlg.get_path(mode = 'Open', wc = FO.JSON_WC)
					print("database path: ", path)
					self.db = IssueDatabase(path)
				except:
					print("everything broke")
				
	def get_possible(self, column_heading: str) -> List[str]:
		return self.db.get_column_names(column_heading)
		
	def set_dirty(self, dirty: bool) -> None:
		self.dirty = dirty
	
	def get_dirty(self) -> bool:
		return self.dirty
		
	def get_title(self) -> str:
		if self.dirty:
			return '* ' + self.title + self.title_suffix
		else:
			return self.title + self.title_suffix
			
	def set_title(self, title: str) -> None:
		self.title = title
		
	def compound_search(self, search: Dict[str, str]) -> List:
		return self.db.compound_search(search)
	
	def get_wcag_link(self, wcag: str) -> str:
		return self.db.get_wcag_link(wcag)
	
	def clear_issue_l(self, override: bool) -> bool:
		if override or not self.dirty:
			self.issue_l = IssueList()
			self.title = 'new'
			self.dirty = False
			self.curr_issue_id = -1
			return True
		else:
			return False
	
	def generate_report(self) -> None:
		order_of_keys: List = [
		PLATFORM,
		USER_TYPE,
		ISSUE_SUMMARY,
		ISSUE_DESCRIPTION,
		STEPS,
		REMEDIATTION,
		SEVERITY,
		CATEGORY,
		BEST_PRACTICE,
		WCAG]
		
		tbw: List[List] = [] #to be written
		tbw.append(order_of_keys)
		for entry in self.issue_l:
			tbw.append(export.dict_to_list(order_of_keys,entry))
		p_name = r'C:\Users\p2763554\Documents\GitHub\TestingTool\excl.xls'
		dlg = FO.FileDialog()
		p_name = dlg.get_path(mode = 'New', wc = FO.XLS_WC)
		
		export.generate(p_name,tbw)
		
	def replace_issue_list(self, file: IO[str]) -> None:
		self.issue_l.read_issues(file)
	
	def get_issues(self) -> 'IssueList':
		return self.issue_l
		
	def get_issue(self, id: int) -> Dict[str, str]:
		return self.issue_l.get(id)
		
	def close(self) -> None:
		pass
	
	def get_curr_issue_id(self) -> int:
		return self.curr_issue_id
	
	def set_curr_issue_id(self, id: int) -> None:
		self.curr_issue_id = id
	
	def add_issue(self, issue) -> None:
		self.issue_l.add_issue(issue)
	
	def update_issue(self, data) -> None:
		self.issue_l.update_issue(int(self.curr_issue_id), data)
	
	def write_issues(self, file: IO[str]) -> None:
		self.issue_l.write_issues(file)	
		
	def remove_issue(self, id: int) -> None:
		self.issue_l.remove_issue(id)
	
def main() -> None:
	hub = Hub()

if __name__ == "__main__":
	main()
	
