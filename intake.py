import glob, os
from tinydb import TinyDB, Query
from typing import List

ISSUE_ID = "IssueID"
USER_TYPE = "UserType"
CATEGORY = "Category"
BEST_PRACTICE = "BestPractice"
PLATFORM = "Platform"
IMPACT = "Impact"
WCAG = "WCAG"
LINK = "Link"

def read_xlsx(file):
	'''given an excel file path, return an array in the format data[sheet][row][column]'''
	import xlrd
	book = xlrd.open_workbook(file)
	data = [] #type: List[List]
	for i in range(book.nsheets):
		sheet = book.sheet_by_index(i)
		data.append([])
		for row in range(sheet.nrows):
			r = sheet.row_values(row)
			br = False #break if not all of the lements are filled in
			for elem in r:
				if not elem:
					br = True
			if br:
				continue
			data[i].append(r)
	return data
	
def build_db(issues, pathname: str) -> None:
	with TinyDB(pathname) as db:
		if not len(db) > 1:
			for i, issue in enumerate(issues):
				db.insert({ISSUE_ID: i, 
							USER_TYPE: issue[0],
							CATEGORY: issue[1],
							BEST_PRACTICE: issue[2],
							PLATFORM: issue[3],
							IMPACT: issue[4],
							WCAG: issue[5],
							LINK: issue[6]})
		db.close()
	
def main() -> None:
	uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])
	files = glob.glob(uppath(__file__, 1) + os.sep + "*.xlsx")
	issues:List = []
	for file in files[1:]:
		print(file)
		data = read_xlsx(file)
		issues = data[0]
	print(len(issues))
	
	pathname = r"C:\Users\p2763554\Documents\Python Scripts\Testing Reporting\db.json"
	build_db(issues, pathname)
	db = TinyDB(pathname)
	Issue = Query()
	result = db.search(Issue.Platform == "Tv")
	user_types = list(set([item['Category'] for item in result[1:]]))
	print(len(user_types))
	for user_type in user_types:
		print(user_type)
		
if __name__ == '__main__':
	main()
