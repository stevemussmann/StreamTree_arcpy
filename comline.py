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
		self.args = parser.parse_args()
		print self.args.streams
		print self.args.points
