use strict; use warnings;
use JSONRegex;
use Test::More;

################################# HELPERS #####################################
sub ok_all_match{
	my ($arrayref, $regex) = @_;
	for my $el (@$arrayref) {
		ok( $el =~ $regex ) or warn "Failed element: $el";
	}
	return 1
}

sub ok_all_mismatch{
	my ($arrayref, $regex) = @_;
	for my $el (@$arrayref) {
		ok( $el !~ $regex ) or warn "Failed element: $el";
	}
	return 1
}

################################## MAIN #######################################
my @fracs = qw(.0 .00 .01 .10 .876 .03247650803824756083476508237465087326450873465082);
	ok_all_match( \@fracs, qr/^$JSONRegex::frac$/ );
my @nonfracs = qw(. 0 7 -8);
	ok_all_mismatch( \@nonfracs, qr/^$JSONRegex::frac$/ );

my @natural_numbers = qw(0 1 100000 1932847 1034972560823765087365087348736083247);
	ok_all_match( \@natural_numbers, qr/^$JSONRegex::natural_number$/ );
my @nonnatural_numbers = (qw(-135 -1 -0 01), @fracs);
	ok_all_mismatch( \@nonnatural_numbers, qr/^$JSONRegex::natural_number$/ );


done_testing;
