#!/bin/zsh


# back out of directories until you arrive at /path/to/prove-math
for ((i=0; i<99; i++))
	do CWD=$(pwd | sed -e 's@.*/@@') # finds the stuff after the last / in pwd
	if [[ $CWD != prove-math ]]
		then cd ..
	fi
done
# complain if you weren't somewhere inside of /path/to/prove-math to begin with
if [[ $CWD = '' ]]
	then
	echo 'You must be inside the prove-math directory before executing this script.'
	exit 2
fi


# convert .scss files to main.css
# instead of doing it manually every time, we will use a watch daemon.  but we should only launch it if it's not running!
IFS=$'\n'
array_of_processes=($(ps | grep 'compass watch'))
IFS=$' \t\n'
number_of_matches=$#array_of_processes
if [[ $number_of_matches = 1 ]] # the one match is the grep process itself!
	then
	cd www
	compass watch &| # In the background, so we can continue.  Disowned, so we won't be waiting on it.
	cd ..
fi # this only fails when babel_watchdog throws an error.  Then i get a SECOND compass process!


# javascript 6 files to 5
# we will use a watchdog, just like compass watch!
IFS=$'\n'
array_of_processes=($(ps | grep 'babel_watchdog'))
IFS=$' \t\n'
number_of_matches=$#array_of_processes
if [[ $number_of_matches = 1 ]]
	then
	zsh build/javascript6to5.zsh
	python3 build/babel_watchdog.py ./www/scripts6 &|
fi


# optimize and minify
os=$(uname)
if [[ $os = FreeBSD ]]
	then
	# node build/r.js -o mainConfigFile=www/scripts/main.js baseUrl=www/scripts/lib name=../main out=www/scripts/main-optimized.min.js generateSourceMap=true preserveLicenseComments=false optimize=uglify2
	node build/r.js -o mainConfigFile=www/scripts/main.js baseUrl=www/scripts/lib name=../main out=www/scripts/main-optimized.min.js generateSourceMap=true preserveLicenseComments=false optimize=uglify2
	echo 'remember to switch "main" to "main-optimized.min" in index.html'
fi

echo 'done updating files on local machine'


if [[ $os != FreeBSD ]]
	then
	open -a "Google Chrome" http://localhost
fi

echo 'done.'
