#! /usr/bin/python

from comline import ComLine
from find_vertices import FindVertices
import sys

def main():
	input = ComLine(sys.argv[1:])
	verts = FindVertices(input.args.points, input.args.streams)
	print verts.vertices
	
main()

raise SystemExit