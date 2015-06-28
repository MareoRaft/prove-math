package JSONRegex;

# regexs to recognize json values (BUT ONLY THE ONES I WILL BE USING):
our $frac = qr(\.\d+);
our $natural_number = qr(0|[1-9]\d*);
our $number = qr($natural_number$frac?);
our $char = qr([^"\\]|\\(?:["\\nt]|u[0-9a-f]{4}));
our $string = qr("$char*");
our $base_value = qr($string|$number|true|false|null);

our $gobble_strings = qr((?:[^"]*$string)*[^"]*); # guarantees that what is immediately after this isn't in the middle of a string
our $nibble_strings = qr((?:[^"]*$string)*?[^"]*?); # reluctant version (first star greedy is ok)
our $gobble_strings_no_braces = qr((?:[^"{}]*$string)*[^"{}]*); # does not allow { or } outside of strings

our $line_containing_comment = qr(^(?<PRECOMMENT>$nibble_strings)//.*)m; # should be used with multi-line option
our $matched_braces = qr((?<MATCHEDBRACES>\{(?:$gobble_strings_no_braces(?&MATCHEDBRACES))*$gobble_strings_no_braces\}));
our $code_with_trailing_comma = qr/^(?<PRETRAILINGCOMMA>$gobble_strings(?:$base_value|\]|\})\s*),(?<POSTTRAILINGCOMMA>\s*[\]\}])/; # should be used with WHILE loop to get ALL trailing commas

1
