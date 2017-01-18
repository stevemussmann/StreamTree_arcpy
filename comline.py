import argparse

class ComLine():
	'Class for implementing command line argument parsing'
	#points = "crb_sites_selected.shp"
	#streams = "crb_streams.shp"
	
	def __init__(self, args):
		parser = argparse.ArgumentParser()
		parser.add_argument("-s", "--streams",
										dest='streams',
										default="crb_streams.shp",
										help="Specify an ESRI shapefile containing connected stream segments (lines)"
										)
		parser.add_argument("-p", "--points",
										dest='points',
										default="crb_sites_selected.shp",
										help="Specify an ESRI shapefile containing sampling localities (points)"
										)
		parser.add_argument("-c", "--code",
										dest='code',
										default="CODE",
										help="Specify the name of the field in the attribute table of your points layer that contains sample site names"
										)
		self.args = parser.parse_args()
		print self.args.streams
		print self.args.points
		print self.args.code
