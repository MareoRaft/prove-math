foreach( @ARGV ){ $destination.="$_ " } $destination =~ s/ $//; #print "\$destination is $destination\n";

sub go{
	my ($pathT,$maxdepth) = @_;
	chdir $pathT;
	for( my $d=1; $d<=$maxdepth; $d++ ){
		my $command = 'ls -d '.  '*/' x $d  .'|grep "'.$destination.'/"';
		my $numSupDirectories = $d-1;
		if( `$command` =~ m@^((?:[^/]+/){$numSupDirectories}$destination/)\n@ ){ return $1 }
	}
	return '';
}

my $startpath = "/Users/Mohith/"; #we include the slash at end because go does not include that at beginning of return. (also good for root)
my $go = go($startpath,5);

if( $go ne '' ){
	my $pathtodest = $startpath.$go; #maxdepth of 5 is a good choice.
	print $pathtodest;
	exit 0;
}

exit 1;

#/ use maxdepth 4
#/Users/ use maxdepth 6 (includes some other things too, but most likely UNWANTED
#/Users/Matthew/ use maxdepth 5
#/Users/Matthew/DesktopFolders/ use as high as you want but if you go too high (9): error message to terminal.
