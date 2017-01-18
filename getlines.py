from __future__ import print_function
import arcpy
import os

class FindLines():
	'Class for identifying stream segments that fall between '
	def __init__(self,vertices,streams,code):
		# set workspace
		arcpy.env.workspace = os.getcwd()
		arcpy.env.overwriteOutput=True
		arcpy.env.XYResolution = "1 Meters"
		arcpy.env.XYTolerance = "1 Meters"
		
		values = self.unique_values(vertices, 'FID')
		ln_values = self.unique_values(streams,'FID')
		st_layer = arcpy.MakeFeatureLayer_management(streams, "stream_layer")
		self.add_field(vertices,"NODES","TEXT",100)
		self.add_field(streams,"Point_A","TEXT",10)
		self.add_field(streams,"Point_B","TEXT",10)
		self.select_lines(values, st_layer,vertices)
		self.replace_null(vertices,code)
		
		pt_layer = arcpy.MakeFeatureLayer_management(vertices, "point_layer")
		self.select_points(ln_values,pt_layer,streams)

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
			print("vertex",value+1,"of",len(values))
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
		
	def replace_null(self,file,field):
		with arcpy.da.UpdateCursor(file, [field]) as cursor:
			for row in cursor:
				if row[0] is None or not str(row[0]).strip():
					row[0] = "NONE"
					cursor.updateRow(row)
		print("Attribute tables updated.")
		
	def select_points(self,values,pt_layer,streams):
		for value in values:
			query = "FID = " + str(value)
			ln_layer = arcpy.MakeFeatureLayer_management(streams, "line_layer", query)
			vert_layer = arcpy.SelectLayerByLocation_management(pt_layer,"INTERSECT",ln_layer,"1 Meters")
			fids = self.unique_values(vert_layer, 'FID')
			print("line",value+1,"of",len(values))
			fields=['FID','Point_A','Point_B']
			with arcpy.da.UpdateCursor(streams, fields) as rows:
				for row in rows:
					if row[0] == value:
						row[1] = str(fids[0])
						row[2] = str(fids[1])
						rows.updateRow(row)