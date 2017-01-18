from __future__ import print_function
import arcpy
import os

class FindLines():
	'Class for identifying stream segments that fall between '
	def __init__(self,vertices,streams):
		# set workspace
		arcpy.env.workspace = os.getcwd()
		arcpy.env.overwriteOutput=True
		arcpy.env.XYResolution = "1 Meters"
		arcpy.env.XYTolerance = "1 Meters"
		
		values = self.unique_values(vertices, 'FID')
		st_layer = arcpy.MakeFeatureLayer_management(streams, "stream_layer")
		self.add_field(vertices,"NODES","TEXT",100)
		self.select_lines(values, st_layer,vertices)

	# Get all values of FIDs in vertices table
	def unique_values(self,table, field):
		with arcpy.da.SearchCursor(table, [field]) as cursor:
			return sorted({row[0] for row in cursor})

	def select_lines(self,values, st_layer,vertices):
		for value in values:
			query = "FID = " + str(value)
			pt_layer = arcpy.MakeFeatureLayer_management(vertices, "point_layer", query)
			ln_layer = arcpy.SelectLayerByLocation_management(st_layer, "INTERSECT", pt_layer, "1 Meters")
			fids = self.unique_values(ln_layer, 'FID')
			print(value+1,"of",len(values))
			sep="|"
			insertion=sep.join(str(x) for x in fids)
			#print(insertion)
			fields=['FID', 'NODES']
			with arcpy.da.UpdateCursor(vertices, fields) as rows:
				for row in rows:
					if row[0] == value:
						row[1] = insertion
						rows.updateRow(row)
			
	def add_field(self,input,fieldname,type,length):
		arcpy.AddField_management(input, fieldname, type, field_length=length)