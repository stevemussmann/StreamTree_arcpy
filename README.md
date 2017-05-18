This program is designed to create the input for the StreamTree program (http://www.montana.edu/kalinowski/Software/StreamTree.htm) by Kalinowski et al. 2008.

Currently this is a work in progress, and is comprised of multiple scripts.  I am in the process of transitioning from Perl to Python code.

The main program, streamtree_arcpy.py, takes as input an ESRI shapefile containing a series of connected streams, and another containing sampling points.
Important notes:
*Every branch of the stream layer must either end at a site in the points file, or end at a place where the river forks to go to multiple points.
*Reticulations in the stream file are not allowed.
