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
babel www/scripts6/lib/profile.js > www/scripts/lib/profile.js &&
babel www/scripts6/lib/d3-and-svg.js > www/scripts/lib/d3-and-svg.js &&
babel www/scripts6/main.js > www/scripts/main.js &&

# optimize and minify
# node build/r.js -o mainConfigFile=www/scripts/main.js baseUrl=www/scripts/lib name=../main out=www/scripts/main-optimized.min.js generateSourceMap=true preserveLicenseComments=false optimize=uglify2 &&


echo 'done updating files on local machine' &&



open http://localhost/index.html &&

echo 'done.'
