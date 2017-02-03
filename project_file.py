from __future__ import print_function
import arcpy
import os

class ProjectFile():
	'Class for projecting a file to the desired new projection'
	def __init__(self,file,projection):
		# set workspace
		arcpy.env.workspace = os.getcwd()
		arcpy.env.overwriteOutput=True
		arcpy.env.XYResolution = "1 Meters"
		arcpy.env.XYTolerance = "1 Meters"
		
		self.projection = projection
		self.file = file

		name,ext = file.split(".")
		out = name + "_projected." + ext
		print(out)
		self.out = out

	def define_projection(self):
		coord_system = arcpy.SpatialReference(self.projection)
		arcpy.Project_management(self.file,self.out,coord_system)
		return self.out