This program is designed to create the input for the StreamTree program (http://www.montana.edu/kalinowski/Software/StreamTree.htm) by Kalinowski et al. 2008.

Currently this is a work in progress, and is comprised of multiple scripts.  I am in the process of transitioning from a sweries of Perl scripts to a single Python program.

The main program, streamtree_arcpy.py, takes as input an ESRI shapefile containing a series of connected streams, and another containing sampling points.
Important notes:
* This requires a valid ArcGIS license to use the arcpy tools.  
* I wrote this using ArcGIS 10.4 and have not tested any older (or newer) versions.
* I have so far only tested the Python components under Windows and the Perl scripts under Linux (Ubuntu).
* Every branch of the stream layer must either end at a site in the points file, or end at a place where the river forks to go to multiple points.
* Reticulations in the stream file are not allowed.

# Steps
1. Run the streamtree_arcpy.py program on your streams .shp and sites .shp files.
2. Run the tracepaths.pl Perl script on the output of streamtree_arcpy.py.  Assuming you have not changed the output file names from step 1, this can be done with the command.  The file sitenames.txt is just a plain text file with a list of all site names that are found in your streams .shp file.  tracepaths.pl will print the paths to STDOUT, so you may want to redirect it to a textfile.
```
./tracepaths.pl -n nodes.txt -b branches.txt -s sitenames.txt > allpaths.txt
```
3. Generate a matrix of genetic distance values in the program of your choice.  Prepare two files:
    1. A lower triangular matrix of genetic distance values named "genetic_distances.txt"
    2. A list of populations in the same order as the rows in the matrix (one population per line) named "pops.txt"
4. Run gen_dist.pl
```
./gen_dist.pl > gendist_pairs.txt
```
5. Run combine_gen_stream_dist.pl.  This will output a file named streamtree_input.txt.  In the process of creating this file, any negative genetic distance values are converted to zeroes.  
6. You should now be able to run Stream Tree.  If you receive an error such as "matrix is singular" it probably means that your original streams .shp file has a dead end that does not connect to a sampling site.
