#! /usr/bin/python

from comline import ComLine
from find_vertices import FindVertices
from getlines import FindLines
from export_table import ExportTable
from project_file import ProjectFile
from calc_dist import CalculateDistance
import sys

def main():
	input = ComLine(sys.argv[1:])
	verts = FindVertices(input.args.points, input.args.streams,input.args.code)
	print verts.vertices
	print verts.splits
	lines = FindLines(verts.vertices,verts.splits,input.args.code)
	exNodes = ExportTable(verts.vertices, "nodes.txt")
	exNodes.export(input.args.code)
	exBranches = ExportTable(verts.splits, "branches.txt")
	exBranches.export(input.args.code)
	
	#project the files into UTM Zone 12N - files must be in projected coordinate system for calculating stream length
	#need to add a command line option for changing the projection
	projection = "NAD 1983 UTM Zone 12N"
	prStreams = ProjectFile(verts.splits,projection)
	proj_streams = prStreams.define_projection()
	prSites = ProjectFile(input.args.points,projection)
	proj_sites = prSites.define_projection()
	
	#calculate stream distance
	dist_streams = CalculateDistance(proj_streams)
	dist_streams.calcdist()
	
main()

raise SystemExit