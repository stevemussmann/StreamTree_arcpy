from __future__ import print_function
#import arcpy
#import os
#from tracePaths import TracePaths

class TracePaths():
	'Class for tracing paths between sites along stream network'
	def __init__(self,sites):
		branches="branches.txt"
		nodes="nodes.txt"
		
		self.branchLines = self.readFile(branches)
		self.nodeLines = self.readFile(nodes)
		self.siteLines = self.readFile(sites)
		
		
	def readFile(self, file):
		tempList = list()
		with open(file) as f:
			tempList = f.readlines()
		tempList = [x.strip() for x in tempList]
		return tempList
		

def main():
	obj = TracePaths("sitenames.txt")
	
	print(obj.branchLines)
	
main()

raise SystemExit