#!/usr/bin/env perl

# This perl script will use regex to convert .pre-json files to .json files

# regex to recognize a json value:
# see json.org !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
my $e = qr([eE][+-]?);
# $digit is \d, so we'll just type \d
# $digits is \d+, so we'll just type \d+
my $exp = qr($e\d+);
my $frac = qr(\.\d+);
my $int = qr(-?\d(?:[1-9]\d+)?);
my $number = qr($int(?:$frac|$exp|$frac$exp));

my $char = qr([^"\\]|\\(?:["\\/bfnrt]|uFOURHEXDIGITS));
my $string = qr("$char*");

my $value = qr($string|$number|$OBJECT|$ARRAY|true|false|null);

my $elements = qr($value(?:\s*,\s*$value)*);
my $array = qr(\[\s*$elements?\s*\]);

my $pair = qr($string\s*:\s*$value);

my $members = qr($pair(?:\s*,\s*$pair)*);
my $object = qr(\{\s*$members?\s*\});


if( '0.9i' =~ $number ){ print 'success' }

# 1. All comments will be deleted

# 2. Commas will be added to the end of all top-level dics

# 3. Everything will be wrapped in a large array

# 4. Lists and arrays where the last element is followed by a comma will have the comma deleted
