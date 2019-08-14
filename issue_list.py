from typing import List, Dict, IO, Iterator, Iterable, Any, Tuple
import json, sys

class IssueList(Iterable):
	NUM = 'num'
	def __init__(self) -> None:
		self.l = [] #type: List[Dict]
		self.count: int = 0 #used as a refernce for creating an index
							#if issues are delete, this wil liekly be wrong
		
	def __str__(self) -> str:
		return str(self.l)
	
	def __len__(self) -> int:
		return len(self.l)
		
	def __iter__(self) -> Iterator:
		return iter(self.l)
		
	def add_issue(self, issue: Dict[str, str]) -> None:
		'''
		issue: a dict of isssue key, value pairs
		return success: boo
		'''
		issue[IssueList.NUM] = int(self.count)
		self.count += 1
		self.l.append(issue)
		
	def remove_issue(self, index: int) -> bool:
		i = -1
		for j, item in enumerate(self.l):
			if item[IssueList.NUM] == index:
				i = j
				break
		if i == -1:
			return False
		self.l.pop(i)
		return True
	
	def find(self, pair: Tuple[str, str]) -> int:
		key, value = pair
		for item in self.l:
			try:
				if item[key] == value:
					return item[IssueList.NUM]
			except KeyError:
				continue
				
	def get(self, num: int) -> Dict[str, str]:
		for issue in self.l:
			if issue[IssueList.NUM] == num:
				return issue
	
	def update_issue(self, num: int, new: Dict[str,str]) -> None:
		for key, value in new.items():
			try:
				self.l[num][key] = value
			except KeyError:
				pass
			
	def write_issues(self, fp: IO[str]) -> None:
		json.dump(self.__dict__,fp)
	
	def read_issues(self, fp: IO[str]) -> None:
		self.__dict__.update(**(json.load(fp)))
	
def main() -> None:
	issue = IssueList()
	issue.add_issue({'Name':'Alice', 'Age': '5'})
	issue.add_issue({'Name':'Bob', 'Age':'3'})
	issue.add_issue({'Name':'Charlie', 'Age': '7'})
	issue.add_issue({'Name':'Dennis', 'Age': '6'})
	i = issue.find(('Name', 'Bob'))
	issue.remove_issue(i)
	issue.write_issues(sys.stdout)
	print('')
	
if __name__ == "__main__":
	main()
		