from typing import List, Dict, IO, Iterator, Iterable, Any
import json, sys

class IssueList(Iterable):
	def __init__(self) -> None:
		self.l = [] #type: List[Dict]
		
	def __str__(self) -> str:
		return str(self.l)
	
	def __len__(self) -> int:
		return len(self.l)
		
	def __iter__(self) -> Iterator:
		return iter(self.l)
		
	def add_issue(self, issue: Dict[str, str]) -> bool:
		'''
		issue: a dict of isssue key, value pairs
		return success: boo
		'''
		self.l.append(issue)
		return True
		
	def write_issues(self, fp: IO[str]) -> None:
		json.dump(self.l,fp)
	
	def read_issues(self, fp: IO[str]) -> None:
		self.l = json.load(fp)
	
def main() -> None:
	issue = IssueList()
	f = open(r'C:\Users\p2763554\Documents\GitHub\TestingTool\test.json')
	issue.read_issues(f)
	issue.write_issues(sys.stdout)
	print(len(issue))
	for item in issue:
		print(item)
	
if __name__ == "__main__":
	main()
		