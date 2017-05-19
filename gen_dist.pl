#!/usr/bin/perl

use warnings;
use strict;

my $pops = "pops.txt";
my $matrix = "genetic_distances.txt";

my @poparray;
my @matrixarray;

open( FILE, $pops ) or die "Can't open $pops: $!\n\n";
while(my $line = <FILE> ){
	chomp $line;
	push @poparray, $line;
}
close FILE;

open( FILE, $matrix ) or die "Can't open $matrix: $!\n\n";
while(my $line = <FILE> ){
	chomp $line;
	push @matrixarray, $line;
}
close FILE;

for( my $i=0; $i<@matrixarray; $i++ ){
	my @line = split( /\s+/, $matrixarray[$i]);
	for( my $j=0; $j<@line; $j++ ){
		if($i != $j ){
			print $poparray[$i], "\t", $poparray[$j], "\t", $line[$j], "\n";
		}
	}
}

exit;
