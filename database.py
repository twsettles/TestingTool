import wx
from typing import Dict, List
from tinydb import TinyDB, Query, where

import intake

class IssueDatabase(TinyDB):
	def __init__(self,*args, **kwds):
		if (not args) and (not kwds):
			pass
		else:
			TinyDB.__init__(self,*args, **kwds)
	
	def compound_search(self, dd: Dict[str, str]) -> List:
		"""
		given a dictionary of search terms, returns a list of the results
		"""
		result = [] #type: List
		to_delete = [] #type: List
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
		
	def get_wcag_link(self, selection: str):
		"""
		Updates the WCAG link field, based on the WCAG criteria choice
		"""
		if selection == "All":
			return ''
		results = self.search(where(intake.WCAG) == selection)
		if len(results):
			return results[0][intake.LINK]
		else:
			return ''
