#! /usr/bin/python

from comline import ComLine
from find_vertices import FindVertices
from getlines import FindLines
import sys

def main():
	input = ComLine(sys.argv[1:])
	verts = FindVertices(input.args.points, input.args.streams,input.args.code)
	print verts.vertices
	print verts.splits
	lines = FindLines(verts.vertices,verts.splits)
	
main()

raise SystemExit