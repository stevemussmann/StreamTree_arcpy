#! /usr/bin/perl

use warnings;
use strict;
use Getopt::Std;
use Data::Dumper;

# kill program and print help if no command line arguments were given
if( scalar( @ARGV ) == 0 ){
  &help;
  die "Exiting program because no command line options were used.\n\n";
}

# take command line arguments
my %opts;
getopts( 'b:ho:p:', \%opts );

# if -h flag is used, or if no command line arguments were specified, kill program and print help
if( $opts{h} ){
  &help;
  die "Exiting program because help flag was used.\n\n";
}

# parse the command line
my( $branch, $out, $paths ) = &parsecom( \%opts );

#print $branch, "\n";
#print $paths, "\n";

#declare variables
my @branchlines; #holds lines from branch file
my @pathslines; #holds lines from node file

my %bl; #holds length of each branch
my %trace; #holds path trace between each two points

#variables for branches
&filetoarray($branch, \@branchlines);
&filetoarray($paths, \@pathslines);

shift @branchlines;

foreach my $line( @branchlines ){
	my @temp = split( /,/, $line );
	$bl{$temp[0]} = $temp[4];
}

foreach my $line( @pathslines ){
	my @temp = split( /,/, $line );
	my $pair = join( ",", $temp[0], $temp[1] );
	shift( @temp );
	shift( @temp );
	my $list = join( ",", @temp );
	$trace{$pair} = $list;
}


open( OUT, '>', $out ) or die "Can't open $out: $!\n\n";
foreach my $pair( sort keys %trace ){
	my @temp = split( /,/, $trace{$pair} );
	my $dist=0;
	foreach my $branch( @temp ){
		$dist+=$bl{$branch};
	}
	print OUT $pair, ",", $dist,"\n";
}
close OUT;

#$print Dumper( \%bl );

exit;

#####################################################################################################
############################################ Subroutines ############################################
#####################################################################################################

# subroutine to print help
sub help{
  
  print "\nstreamdist.pl is a perl script developed by Steven Michael Mussmann\n\n";
  print "To report bugs send an email to mussmann\@uark.edu\n";
  print "When submitting bugs please include all input files, options used for the program, and all error messages that were printed to the screen\n\n";
  print "Program Options:\n";
  print "\t\t[ -b | -h | -o | -p ]\n\n";
  print "\t-b:\tUse this to specify branch length file (required).\n\n";
  print "\t-h:\tUse this flag to display this help message.\n";
  print "\t\tThe program will die after the help message is displayed.\n\n";
  print "\t-o:\tUse this flag to specify the output file name.\n";
  print "\t\tIf no name is provided, output will be written to \"output.txt\".\n\n";
  print "\t-p:\tUse this flag to specify the list of paths between sites (required).\n\n";
  
}

#####################################################################################################
# subroutine to parse the command line options

sub parsecom{ 
  
  my( $params ) =  @_;
  my %opts = %$params;
  
  # set default values for command line arguments
  my $branch = $opts{b} || die "No branch file specified.\n\n"; #used to specify tab-delimited population map file  

  my $out = $opts{o} || "distances.txt"; #used to specify output file name.  If no name is provided, the file extension ".genepop" will be appended to the input file name.

  my $paths = $opts{p} || die "No paths file specified.\n\n";

  return( $branch, $out, $paths );

}

#####################################################################################################
# subroutine to put file into an array

sub filetoarray{

  my( $in, $array ) = @_;

  # open the input file
  open( FILE, $in ) or die "Can't open $in: $!\n\n";

  # loop through input file, pushing lines onto array
  while( my $line = <FILE> ){
    chomp( $line );
    next if($line =~ /^\s*$/);
    push( @$array, $line );
  }
  close FILE;

}

#####################################################################################################

