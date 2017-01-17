#! /usr/bin/python

from __future__ import print_function
import arcpy
from arcpy import env
import os
import sys
import getopt
import re

# get the working directory
wd = os.getcwd()

# set workspace
env.workspace = wd
arcpy.env.overwriteOutput=True
arcpy.env.XYResolution = "1 Meters"
arcpy.env.XYTolerance = "1 Meters"


# set default names of input files
points = "crb_sites_selected.shp"
streams = "crb_streams.shp"

# parse the command line arguments
def comline(argv):
	try:
		opts, args = getopt.getopt(argv, "hp:s:", ["help", "vertices=", "streams="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-p", "--points"):
			global vertices
			inshp = arg
		elif opt in ("-s", "--streams"):
			global streams
			names = arg
	source = "".join(args)

# define the usage to print for the help message
def usage():
	print ("This is the usage")

# parse the command line
comline(sys.argv[1:])

def dissolve_lines(streams,out):
	print("Dissolving input streams file", streams)
	print("")
	arcpy.Dissolve_management(streams, out, "", "", "SINGLE_PART")
	return out

def snap_points(points, dissolved):
	print("Snapping points file", points, "to", dissolved)
	print("")
	arcpy.Snap_edit(points, [[dissolved, "VERTEX", "2 Kilometers"]])

	
def split_line(points, dissolved,out):
	print("Splitting", dissolved, "at", points, "and writing to", out)
	print("")
	arcpy.SplitLineAtPoint_management(dissolved,points,out,"1 Meters")
	return out

def end_points(splits,out):
	print("Making end points")
	print("")
	arcpy.FeatureVerticesToPoints_management(splits,out,"BOTH_ENDS")
	return out
	
def add_xy(input):
	print("Adding XY coordinates to", input)
	print("")
	arcpy.AddXY_management(input)
	
def remove_identical(endpoints):
	print("Removing redundant endpoints from", endpoints)
	print("")
	arcpy.DeleteIdentical_management(endpoints,["POINT_X","POINT_Y"],"1 Meters")
	
def erase_points(endpoints,points,out):
	print("Removing points in", endpoints, "that are redundant with sampling locations")
	print("")
	arcpy.Erase_analysis(endpoints,points,out,"1 Meters")
	return out
	
def merge_points(erased,points,out):
	print("Merging into final output")
	print("")
	fieldMappings = arcpy.FieldMappings()#create fieldmapping object
	fieldMappings.addTable(erased)#get fields from erased
	fieldMappings.addTable(points)#get fields from points
	for field in fieldMappings.fields:
		if field.name not in ["POINT_X","POINT_Y","CODE"]:
			fieldMappings.removeFieldMap(fieldMappings.findFieldMapIndex(field.name))
	arcpy.Merge_management([erased,points],out,fieldMappings)
	
def main():
	dissolved = dissolve_lines(streams, "streams_dissolve.shp") #dissolve a streams layer with many line segments
	snap_points(points, dissolved)#snap points to the streams to ensure they will accurately split the lines
	splits = split_line(points,dissolved,"split_streams.shp") #split all lines at the sampling sites
	endpoints = end_points(splits,"end_points.shp") #make endpoints for resulting split streams from previous command
	add_xy(endpoints) #add XY cooridnates to attribute table of the endpoints that were created for all lines
	add_xy(points) #add XY coordinates to attribute table of sampling sites
	remove_identical(endpoints) #remove redundant points at ends of stream segments
	erased = erase_points(endpoints,points,"end_points_dissolve_erase.shp")
	merge_points(erased,points,"all_vertices.shp")
		

main()
		
raise SystemExit