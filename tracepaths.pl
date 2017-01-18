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
getopts( 'b:hn:o:s:', \%opts );

# if -h flag is used, or if no command line arguments were specified, kill program and print help
if( $opts{h} ){
  &help;
  die "Exiting program because help flag was used.\n\n";
}

# parse the command line
my( $out, $branch, $node, $sites ) = &parsecom( \%opts );

#declare variables
my @branchlines; #holds lines from branch file
my @nodelines; #holds lines from node file
my @siteslines; 

#variables for branches
my @branchnums; #holds node numbers for all branches.  Array index corresponds to FID for branch
my @sites; #holds site present at each node (if any).  Array index corresponds to FID for node
my @paths; #holds the FID for each branch connected to the node.  Array index corresponds to FID for node

&filetoarray($branch, \@branchlines);
&filetoarray($node, \@nodelines);
&filetoarray($sites, \@siteslines);

shift @branchlines;
shift @nodelines;
my @sites2 = @siteslines;

#put a comma-delimited list of the two nodes at the end of each branch into the @branchnums array
foreach my $line( @branchlines ){
	my @temp = split(/,/, $line);
	my $nodes = join(',', $temp[2], $temp[3]);
	push( @branchnums, $nodes );
}

foreach my $line( @nodelines ){
	my @temp = split(/,/, $line);
	push( @sites, $temp[3] ); #put site number on @sites array
	push( @paths, $temp[4] ); #put list of branches connected to the node onto @paths array
}

foreach my $start(@siteslines){
	shift @sites2; #pop off the first site so that only unique pairs are compared
	foreach my $target(@sites2){
		my $prevbranch = "-9"; #needs a number or else it bitches about non-numeric comparison
		my $startid;
		my $allprevnodes = -9;
		my $allprevbranches = -9;
		for(my $i=0; $i<@sites; $i++){
			if($sites[$i] eq $start){
				$startid = $i;
			}
		}
		my $string = join(',', $start, $target);
		&findpath(\@branchnums, \@sites, \@paths, $target, $startid, $string, $prevbranch, $allprevnodes, $allprevbranches );
	}
}

exit;

#####################################################################################################
############################################ Subroutines ############################################
#####################################################################################################

# subroutine to print help
sub help{
  
  print "\nmapcount.pl is a perl script developed by Steven Michael Mussmann\n\n";
  print "To report bugs send an email to mussmann\@email.uark.edu\n";
  print "When submitting bugs please include all input files, options used for the program, and all error messages that were printed to the screen\n\n";
  print "Program Options:\n";
  print "\t\t[ -b | -h | -n | -o | -s ]\n\n";
  print "\t-b:\tUse this to specify branch file (required).\n\n";
  print "\t-h:\tUse this flag to display this help message.\n";
  print "\t\tThe program will die after the help message is displayed.\n\n";
  print "\t-n:\tUse this flag to specify the node file (required).\n\n";
  print "\t-o:\tUse this flag to specify the output file name.\n";
  print "\t\tIf no name is provided, output will be written to \"output.txt\".\n\n";
  print "\t-s:\tUse this flag to specify list of site names (required).\n\n";
  
}

#####################################################################################################
# subroutine to parse the command line options

sub parsecom{ 
  
  my( $params ) =  @_;
  my %opts = %$params;
  
  # set default values for command line arguments
  my $branch = $opts{b} || die "No branch file specified.\n\n"; #used to specify tab-delimited population map file  

  my $node = $opts{n} || die "No node file specified.\n\n";

  my $out = $opts{o} || "branches.out"  ; #used to specify output file name.  If no name is provided, the file extension ".genepop" will be appended to the input file name.

  my $sites = $opts{s} || die "No sites file specified.\n\n";

  return( $out, $branch, $node, $sites );

}

#####################################################################################################
# subroutine to put file into an array

sub filetoarray{

  my( $infile, $array ) = @_;

  
  # open the input file
  open( FILE, $infile ) or die "Can't open $infile: $!\n\n";

  # loop through input file, pushing lines onto array
  while( my $line = <FILE> ){
    chomp( $line );
    next if($line =~ /^\s*$/);
    push( @$array, $line );
  }
  close FILE;

}

#####################################################################################################
# recursive function to find path

sub findpath{

	my( $branches, $sites, $paths, $target, $current, $string, $prevbranch, $allprevnodes, $allprevbranches ) = @_;
	
	if($prevbranch != -9){
		$string .= ",";
		$string .= $prevbranch;
	}

	#take an input of previous nodes traversed, put into hash for checking
	$allprevnodes .= ",";
	$allprevnodes .= $current;
	my %nodehash;
	my @temp1 = split(/,/, $allprevnodes);
	foreach my $item(@temp1){
		$nodehash{$item}++;
	}

	#take an input of previous branches traversed, put into hash for checking
	$allprevbranches .= ",";
	$allprevbranches .= $prevbranch;
	my %branchhash;
	my @temp2 = split(/,/, $allprevbranches);
	foreach my $item(@temp2){
		$branchhash{$item}++;
	}

	#check if destination is present at current node
	if($$sites[$current] eq $target){
		print $string, "\n";
	}else{
		my @tempbranches = split(/\|/, $$paths[$current]);
		foreach my $index(@tempbranches){
			if(!(exists($branchhash{$index}))){
				my @tempnodes = split(/,/, $$branches[$index]);
				foreach my $node(@tempnodes){
					if(!(exists($nodehash{$node}))){
						$current = $node;
					}
				}
				$prevbranch = $index; #calculate new $prevbranch
				&findpath($branches, $sites, $paths, $target, $current, $string, $prevbranch, $allprevnodes, $allprevbranches );
			}
		}
	}
}

#####################################################################################################
