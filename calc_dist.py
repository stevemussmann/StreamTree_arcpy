from __future__ import print_function
import arcpy
import os

class CalculateDistance():
	'Class for calculating distance of streams'
	def __init__(self,file):
		# set workspace
		arcpy.env.workspace = os.getcwd()
		arcpy.env.overwriteOutput=True
		arcpy.env.XYResolution = "1 Meters"
		arcpy.env.XYTolerance = "1 Meters"
		
		self.file = file
		print(file)

	def calcdist(self):
		arcpy.AddField_management(self.file,"Length_KM","FLOAT")
		arcpy.CalculateField_management(self.file,"Length_KM","!shape.length@kilometers!","PYTHON_9.3")