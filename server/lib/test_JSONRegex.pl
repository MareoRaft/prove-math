################################# IMPORTS #####################################
use strict; use warnings;
use JSONRegex;
use Test::More;

################################# HELPERS #####################################
sub concat_cartesian_product{
	my ($ar1, $ar2) = @_;
	my @result = ();
	for my $e1 (@$ar1) {
		for my $e2 (@$ar2) {
			push @result => $e1.$e2
		}
	}
	return @result
}

sub ok_all_match{
	my ($arrayref, $regex, $name) = @_;
	for my $el (@$arrayref) {
		ok( $el =~ $regex ) or warn "Element $el should be a $name, but does not match $regex";
	}
	return 1
}

sub ok_all_mismatch{
	my ($arrayref, $regex, $name) = @_;
	for my $el (@$arrayref) {
		ok( $el !~ $regex ) or warn "Element $el should NOT be a $name, but matches $regex";
	}
	return 1
}

################################## MAIN #######################################
my @fracs = qw(.0 .00 .01 .10 .876 .03247650803824756083476508237465087326450873465082);
	ok_all_match( \@fracs, qr/^$JSONRegex::frac$/, 'frac' );
my @nonfracs = qw(. 0 7 -8 .t 6.);
	ok_all_mismatch( \@nonfracs, qr/^$JSONRegex::frac$/, 'frac' );

my @natural_numbers = qw(0 1 100000 1932847 1034972560823765087365087348736083247);
	ok_all_match( \@natural_numbers, qr/^$JSONRegex::natural_number$/, 'natural_number' );
my @nonnatural_numbers = (@fracs, qw(-135 -1 -0 01 5l 7.));
	ok_all_mismatch( \@nonnatural_numbers, qr/^$JSONRegex::natural_number$/, 'natural_number' );

my @numbers = (@natural_numbers, concat_cartesian_product(\@natural_numbers, \@fracs)); # fracs are NOT numbers
	ok_all_match( \@numbers, qr/^$JSONRegex::number$/, 'number' );
my @nonnumbers = qw(-135 -1 -0 01 . .p l 23.l 45. 0x11 b11);
	ok_all_mismatch( \@fracs, \@nonnatural_numbers, qr/^$JSONRegex::natural_number$/, 'number' );

my @chars = qw(' { p 7 9 % @ ! ~ ` \\\\ \\n \\t \\u9753); # qw performs qq quotes, so ESCAPING IS NECESSARY
	ok_all_match( \@chars, qr/^$JSONRegex::char$/, 'char' );
my @nonchars = qw('' {} pp 17 堇 袈 \\ \\\\n \\u975 \\b \\w \\r " \\\\u9999);
	ok_all_mismatch( \@nonchars, qr/^$JSONRegex::char$/, 'char' );

my @prestrings = (@chars, concat_cartesian_product(\@chars, \@chars), qw[hello 918234 IGI(*&* (*&* 70\\u9988h], 'i have spaces', '');
my @strings = map { '"'.$_.'"' } @prestrings;
	ok_all_match( \@strings, qr/^$JSONRegex::string$/, 'string' );
my @prenonstrings = qw(堇 袈\\ \\\\n \\u98 \\b \\y " \\\\u7523 pop∢pop);
my @nonstrings = map { '"'.$_.'"' } @prenonstrings;
	ok_all_mismatch( \@nonstrings, qr/^$JSONRegex::string$/, 'string' );


done_testing;
