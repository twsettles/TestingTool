import xlwt
from typing import List, Dict

def main() -> None:
	pathname: str = r'C:\Users\p2763554\Documents\GitHub\TestingTool\excl.xls'
	size: int = 10
	d = [[i*size + j for j in range(size)] for i in range(size)]
	#generate(pathname, d)
	
	keys = ['Apple', "Banana", "Carrot"]
	dic = {"Banana": '14', "Apple":'1', "Carrot": '100'}
	print(dict_to_list(keys, dic))

def generate(pathname: str, data: List[List]) -> None:
	'''
	Writes to the given pathname
	data is in the form of the inner list is earch row
	'''
	book = xlwt.Workbook()
	s1 = book.add_sheet("Sheet 1")
	for i, line in enumerate(data):
		for j, cell in enumerate(line):
			s1.write(i,j,cell)
	book.save(pathname)
	
def dict_to_list(keys: List, d: Dict) -> List:
	'''
	Given an order of keys, return a list of the values of the dict
	'''
	retval: List = []
	for key in keys:
		try:
			retval.append(d[key])
		except KeyError:
			retval.append('')
	return retval

if __name__ == "__main__":
	main()
	