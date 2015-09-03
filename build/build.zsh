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


# convert javascript 6 files to 5
babel www/scripts6/lib/data.js > www/scripts/lib/data.js &&
babel www/scripts6/lib/user.js > www/scripts/lib/user.js &&
babel www/scripts6/lib/profile.js > www/scripts/lib/profile.js &&
babel www/scripts6/lib/d3-and-svg.js > www/scripts/lib/d3-and-svg.js &&
babel www/scripts6/main.js > www/scripts/main.js &&

# convert .scss files to main.css
# instead of doing it manually every time, we will use a watch daemon.  but we should only launch it if it's not running!
IFS=$'\n'
array_of_processes=($(ps | grep 'compass watch'))
number_of_matches=$#array_of_processes
if [[ $number_of_matches = 1 ]]
	then
	cd www
	compass watch & # in the background, so we can continue...
	cd ..
fi
IFS=$' \t\n'

# optimize and minify
# node build/r.js -o mainConfigFile=www/scripts/main.js baseUrl=www/scripts/lib name=../main out=www/scripts/main-optimized.min.js generateSourceMap=true preserveLicenseComments=false optimize=uglify2 &&


echo 'done updating files on local machine' &&



open -a "Google Chrome" http://localhost/index.html &&

echo 'done.'
