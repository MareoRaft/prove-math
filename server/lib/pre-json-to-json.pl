#!/usr/bin/env perl
# This perl script will use regex to convert .pre-json files to .json files
################################# IMPORTS #####################################
use strict; use warnings;
use JSONRegex;

################################# HELPERS #####################################
sub read_file{
	my ($file_path) = @_;
	open( my $IN, '<', $file_path ) or die "Could not open $file_path";
		local $/ = undef;
		my $file_contents = <$IN>;
	close( $IN );
	return $file_contents
}

sub write_file{
	my ($file_path, $file_contents) = @_;
	open( my $OUT, '>', $file_path ) or die "Could not open $file_path";
		print $OUT $file_contents;
	close( $OUT );
	return 1
}

################################## MAIN #######################################
# 0. Read the .pre-json file into $input
my $file_path = $ARGV[0];
if( $file_path !~ /\.pre-json$/ ){ die 'You must input a .pre-json file.' }
my $input = read_file($file_path)

# 1. All comments will be deleted
$input =~ s|$JSONRegex::line_containing_comment|$+{PRECOMMENT}|mg;

# 2. Commas will be added to the end of all top-level dics
$input =~ s/$JSONRegex::matched_braces/$&,/g; # this would naturally pick only the top-level dics

# 3. Everything will be wrapped in a large array
$input = "[\n\n$input\n\n]";

# 4. Objects/Arrays where the last member/element is followed by a comma will have the comma deleted
while( $input =~ s/$JSONRegex::code_with_trailing_comma/$+{PRETRAILINGCOMMA}$+{POSTTRAILINGCOMMA}/ ){} # i think gobble and nibble will have the same performance in this situation

# 5. Write a file with the same name, but ending in .json
$file_path =~ s/\.pre-json$/.json/;
write_file($file_path, $input);


