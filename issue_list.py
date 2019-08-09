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
		
	def write_issues(self, fp: IO[str]) -> None:
		json.dump(self.l,fp)
	
	def read_issues(self, fp: IO[str]) -> None:
		self.l = json.load(fp)
	
def main() -> None:
	issue = IssueList()
	f = open(r'C:\Users\p2763554\Documents\GitHub\TestingTool\test.json')
	#issue.read_issues(f)
	issue.add_issue({'foo':'bar'})
	issue.add_issue({'spam':'eggs'})
	issue.add_issue({'a':'b'})
	issue.add_issue({'bacon':'cheese'})
	i = issue.find(('a','b'))
	issue.remove_issue(i)
	issue.write_issues(sys.stdout)
	print('')
	
if __name__ == "__main__":
	main()
		