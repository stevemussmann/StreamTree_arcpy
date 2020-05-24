from __future__ import print_function

from collections import OrderedDict
import copy

#import arcpy
#import os
#from tracePaths import TracePaths

class TracePaths():
	'Class for tracing paths between sites along stream network'
	def __init__(self,sites):
		branches="branches.txt"
		nodes="nodes.txt"
		
        #lists to hold contents of files
		self.branchLines = self.readFile(branches)
		self.nodeLines = self.readFile(nodes)
		self.siteLines = self.readFile(sites)
		self.sites2 = copy.deepcopy(self.siteLines)
		
		#variables for branches
		self.branchnums = OrderedDict() #holds node numbers for all branches. Key = FID for branch.
		self.sites = OrderedDict() #holds site present at each node (if any). Key = FID for node.
		self.paths = OrderedDict() #holds the FID for each branch connected to the node. Key = FID for node.
		
		#variable for final output
		self.finalPaths = list()
		
		#process the input files
		self.procBranchnums()
		self.procNodes()
		self.pw = self.calcPairwise()
		
	def calcPairwise(self):
		pw = ((len(self.siteLines))*((len(self.siteLines))-1))/2
		return pw
		
	def readFile(self, file):
		tempList = list()
		with open(file) as f:
			tempList = f.readlines()
		tempList = [x.strip() for x in tempList]
		return tempList
		
	def procBranchnums(self):
		self.branchLines.pop(0)
		for line in self.branchLines:
			temp = line.split(',')
			FID = temp.pop(0)
			temp.pop(0)
			nodes = ",".join(temp)
			self.branchnums[FID] = nodes
			
	def procNodes(self):
		self.nodeLines.pop(0)
		for line in self.nodeLines:
			temp = line.split(',')
			FID = temp.pop(0)
			self.sites[FID] = temp[2]
			self.paths[FID] = temp[3]
			
	def traverse(self):
		print("Entry point for recursion")
		for start in self.siteLines:
			self.sites2.pop(0)
			for target in self.sites2:
				prevbranch = "-9"
				startid = ""
				allprevnodes = "-9"
				allprevbranches = "-9"
				for FID,site in self.sites.items():
					if site == start:
						startid = FID
				string = start + "," + target
				self.findPath(target, startid, string, prevbranch, allprevnodes, allprevbranches)
				
	def findPath(self, target, current, string, prevbranch, allprevnodes, allprevbranches):
		#print("Execute findPath here")
		
		if prevbranch != "-9":
			string = string + "," + prevbranch
		#print(string)
		
		# take an input of previous nodes traversed, and put into list for checking
		allprevnodes = allprevnodes + "," + current
		nodeList = allprevnodes.split(",")
		
		# take an input of previous branches traversed, put into list for checking
		allprevbranches = allprevbranches + "," + prevbranch
		branchList = allprevbranches.split(",")
		
		# check if destination is present at current node
		if self.sites[current] == target:
			self.finalPaths.append(string)
			#print(string)
		else:
			tempbranches = self.paths[current].split("|")
			for index in tempbranches:
				if index not in branchList:
					#print(branchList)
					try:
						tempnodes = self.branchnums[index].split(",")
						for node in tempnodes:
							if node not in nodeList:
								current = node
						prevbranch = index #calculate new prevbranch
						self.findPath(target, current, string, prevbranch, allprevnodes, allprevbranches)
					except:
						failure=string.split(",")
						print("")
						print("***************************************************************************************************")
						print("FATAL ERROR:")
						printstring = "Recursion failed on the path from " + failure[0] + " to " + failure[1] + "."
						print(printstring)
						print("The path (including branch numbers) so far was:")
						print(string)
						print("Check your input .shp streams file to make sure it is possible to travel between these two points.")
						print("***************************************************************************************************")
						raise SystemExit
		

def main():
	obj = TracePaths("sitenames.txt")
	
	#sites2 = copy.deepcopy(obj.siteLines)
	#obj.sites2.pop(0)
	
	#print(obj.siteLines)
	#print(obj.sites2)
	
	obj.traverse()
	print(len(obj.finalPaths))
	print(obj.pw)
	
main()

raise SystemExit