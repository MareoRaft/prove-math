#!/usr/bin/env perl
# This perl script will use regex to convert .pre-json files to .json files
################################# IMPORTS #####################################
use strict; use warnings;
use lib::JSONRegex;

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
my $file_path = $ARGV[0] // die 'You must input a file path argument. For example, "./pre-json-to-json.pl myfile.pre-json"';
if( $file_path !~ /\.pre-json$/ ){ die 'You must input a .pre-json file.' }
my $input = read_file($file_path);

# 1. All comments will be deleted, (allowing illegal sloshes in strings)
$input =~ s|$JSONRegex::line_containing_comment_with_illegal_sloshes_allowed|$+{PRECOMMENT}|mg;

# 2. Look for illegal sloshes in strings: \ followed by anything other than \, ", n, or t
while( $input =~ s/^($JSONRegex::gobble_mid_strings)$JSONRegex::illegal_slosh/$1\\\\/ ){}
# for n and t, we have to be smarter, so we interpret a lowecase letter as a latex command.  An actual newline followed by a lowercase letter could not be correct.  It is incorrect grammar.
$input =~ s/(?<!\\)\\(?=[nt][a-z])/\\\\/g;

# 3. Look for newlines within strings, replace them with \n
# 3.5 Look for tabs within strings, replace them with \t
while( $input =~ s/^($JSONRegex::gobble_mid_strings)\r?(?:(\n)|(\t))/ "$1\\" . "n" x!! $2 . "t" x!! $3 /e ){}

# 4. Commas will be added to the end of all top-level dics
$input =~ s/$JSONRegex::matched_braces/$&,/g; # this would naturally pick only the top-level dics

# 5. Everything will be wrapped in a large array
$input = "[\n\n$input\n\n]";

# 6. Everything will be wrapped in a dictionary with key "nodes"
$input = qq({\n"nodes":\n\n$input\n\n});

# 7. Objects/Arrays where the last member/element is followed by a comma will have the comma deleted
while( $input =~ s/$JSONRegex::code_with_trailing_comma/$+{PRETRAILINGCOMMA}$+{POSTTRAILINGCOMMA}/ ){} # i think gobble and nibble will have the same performance in this situation

# 8. Write a file with the same name, but ending in .json
$file_path =~ s/\.pre-json$/.json/;
write_file($file_path, $input);


