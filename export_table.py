from __future__ import print_function
import arcpy
import csv
import os

class ExportTable():
	'Class to output table as csv from a shapefile'
	def __init__(self,shapefile,outfile):
		arcpy.env.workspace = os.getcwd()
		arcpy.env.overwriteOutput=True
		self.shp = shapefile
		self.out = outfile
		
	def export(self,code):
		fields = arcpy.ListFields(self.shp)
		#for field in fields:
		#	print(field.name)
		field_names = [field.name for field in fields if field.name not in ["Shape"]]
		
		with open(self.out, 'wb+') as file:
			w = csv.writer(file)
			w.writerow(field_names)
			
			for row in arcpy.SearchCursor(self.shp):
				#if field.name not in ["POINT_X","POINT_Y",code]:
				field_vals = [row.getValue(field.name) for field in fields if field.name not in ["Shape"]]
				w.writerow(field_vals)
			del row