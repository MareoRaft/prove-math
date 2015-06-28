#!/usr/bin/env perl
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

my @slosh_followers = qw(\\ " u8495 n t uabf3);
	ok_all_match( \@slosh_followers, qr/^$JSONRegex::slosh_follower$/, 'slosh_follower' );
my @nonslosh_followers = qw(\\\\ u u895 b p d uabg3 a l);
	ok_all_mismatch( \@nonslosh_followers, qr/^$JSONRegex::slosh_follower$/, 'slosh_follower' );

my @chars = qw(' { p \\" 7 9 % @ ! ~ ` \\\\ \\n \\t \\u9753); # qw performs qq quotes, so ESCAPING IS NECESSARY
	ok_all_match( \@chars, qr/^$JSONRegex::char$/, 'char' );
my @nonchars = qw('' {} pp 17 堇 袈 \\ \\\\n \\u975 \\b \\w \\r " \\\\u9999);
	ok_all_mismatch( \@nonchars, qr/^$JSONRegex::char$/, 'char' );

my @prestrings = (@chars, concat_cartesian_product(\@chars, \@chars), qw[hello 918234 IGI(*&* (*&* 70\\u9988h], 'i have spaces', '');
my @strings = map { '"'.$_.'"' } @prestrings;
	ok_all_match( \@strings, qr/^$JSONRegex::string$/, 'string' );
my @prenonstrings = qw(\\u98 "); # there were some inconsistent things here: 堇 袈\\ \\b pop∢pop etc
my @nonstrings = map { '"'.$_.'"' } @prenonstrings;
push @nonstrings => ('this is"t', 'hi \\u', '$ \\frac{x-1}{\\binom nk}$');
	ok_all_mismatch( \@nonstrings, qr/^$JSONRegex::string$/, 'string' );

my @base_values = (@strings, @numbers, qw(true false null));
	ok_all_match( \@base_values, qr/^$JSONRegex::base_value$/, 'base_value' );
my @nonbase_values = qw(" . .0 .1 00 003 h"i hi "h"i" ' h '');
	ok_all_mismatch( \@nonbase_values, qr/^$JSONRegex::base_value$/, 'base_value' );

my @gobble_strings_no_braces = (@strings,
	'',
	'there are no strings here',
	'here is "o\"ne" string',
	'here "are" "two"',
	'"918234 IGI(*&* (*&* 70\\u9988h" and "two" and "three" :,,',
);
my @gobble_strings = (@gobble_strings_no_braces,
	'there {are} no strings here',
	'here} is "one{" string',
	'her}e "are" "two"',
	'"918234 IGI(*&* (*&* 70\\u9988h" and "two{"{ and "three" :,,',
);
	ok_all_match( \@gobble_strings, qr/^$JSONRegex::gobble_strings$/, 'gobble_strings' );
	ok_all_match( \@gobble_strings, qr/^$JSONRegex::nibble_strings$/, 'nibble_strings' );
my @nongobble_strings = (
	'there is half "a str',
	'one "and" a "half',
	'two " 7 9 % @ ! ~ ` \\\\ " "79%@!~`\\\\" um "n a half',
	'"918234 IGI(*&* (*&* 70\\u9988h" and "two" and "thre:,,',
);
	ok_all_mismatch( \@nongobble_strings, qr/^$JSONRegex::gobble_strings$/, 'gobble_strings' );
	ok_all_mismatch( \@nongobble_strings, qr/^$JSONRegex::nibble_strings$/, 'nibble_strings' );

	ok_all_match( \@gobble_strings_no_braces, qr/^$JSONRegex::gobble_strings_no_braces$/, 'gobble_strings_no_braces' );

# non gobble_strings_no_braces ?

my @lines_containing_comment = (
	'this //has',
	'a // comment!',
	'"918234 IGI(*&* (*&* 70\\u9988h" and "two" an// yo',
	'// this is fully commented line',
);
	ok_all_match( \@lines_containing_comment, qr/^$JSONRegex::line_containing_comment$/, 'line_containing_comment' );
my @nonlines_containing_comment = (
	'this has',
	'no comment!',
	'918234 IGI(*&* (*&* 70\\u9988h" and "two" an// yo',
	'"// this is half quoted line',
	'what " // do you want? "',
	'what " // do you want? " ok?',
);
	ok_all_mismatch( \@nonlines_containing_comment, qr/^$JSONRegex::line_containing_comment$/, 'line_containing_comment' );

my @matched_braces = (
	qw({} {{}} {{{}}} {{}{}} {{{}}{}} {{}{}{}} {{}{{}}{{{}}}{{}}{}}),
	qw<{27365} {({}{((}} {oo({}{)}} {p}>,
	'{ kk "}" }', '{"pizza"  "i){" this {} is "{{{{{" sparta! }',
);
	ok_all_match( \@matched_braces, qr/^$JSONRegex::matched_braces$/, 'matched_braces' );
my @mismatched_braces = (
	qw({}} {{{}} {{{}}{} {{}}{}} {{{{}}{}} {{}{}}{}} {{}{{}}{{{}}}{{}}{}}} {{{}{}{}}),
	qw<27365} {({}{((} {o}o"({{)"}} {p"}" {p"}>,
	'{ kk "}" ', '{"pizza"  "i){" this {} is "{{{{{" sparta! "}"',
);
	ok_all_mismatch( \@mismatched_braces, qr/^$JSONRegex::matched_braces$/, 'matched_braces' );

my @codes_with_trailing_comma = ( # keep in mind if the writer doesn't input a value correctly, the trailing comma after it won't be detected!
	'0, ]',
	qq("examples": [\n\t\t\t\t"Example 1","Example 2"\n,  ]),
	qq("Example 1",\n      "Example 2"\n],\n\t\t\t\t}),
	qq(]},],}),
);
	ok_all_match( \@codes_with_trailing_comma, qr/^$JSONRegex::code_with_trailing_comma$/, 'code_with_trailing_comma' );
my @noncodes_with_trailing_comma = (
	'0 ]',
	qq("examples": [\n\t\t\t\t"Example 1","Example 2"\n  ]),
	qq("Example 1",\n      "Example 2"\n],\n\t\t\t\t),
	qq(]},],),
);
	ok_all_mismatch( \@noncodes_with_trailing_comma, qr/^$JSONRegex::code_with_trailing_comma$/, 'code_with_trailing_comma' );



done_testing;
