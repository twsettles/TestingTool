import wx
from typing import *
from tinydb import TinyDB, Query, where

class IssueDatabase(TinyDB):
	def _init__(self,*args, **kwds):
		print("wrapper")
		TinyDB.__init__(self,*args, **kwds)
		self.Issue = Query()
	
	def compound_search(self, dd: Dict):
		"""
		given a dictionary of search terms, returns a list of the results
		"""
		result = []
		to_delete = []
		#remove "All" from the search results
		for k,v in dd.items():
			if (v == "") or (v =="ALL"):
				to_delete.append(k)
		for key in to_delete:
			try:			
				del dd[key]
			except KeyError:
				pass
		#print("Filtering based on:\t" + str(dd))
		if dd: # if things to search
			search_list = []
			for k,v in dd.items():
				search_list.append("(where('"+k+"') == '"+v+"')")
			code = "self.search("+'&'.join(search_list)+")"
			result = eval(code)
		else: # run an unfiltered search
			result = self.empty_search()
		return result
		
	def get_column_names(self, column_title: str):
		"""
		Given a key, return all possible values, as a list
		"""
		result = self.empty_search()
		user_types = list(set([item[column_title] for item in result[1:]]))
		return user_types
	
	def empty_search(self):
		return self.search(Query().IssueID.test(lambda x: True))