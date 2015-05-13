# This script wraps all js files in katex with the define(function(require, exports, module){ ... }) wrapper.

cd ~/programming/javascript/Proof && # but this will need to be replaced, or there should be an understanding that all build files are run from the root of the project, or something

cd build &&

echo 'define(function(require, exports, module){' > wrapbegin.txt &&

echo '}) // end of define' > wrapend.txt &&


list=$(find ../www/scripts/lib/katex -name '*.js') &&

# for file in $list; do
# find . -name '**/*.txt' -print0 | xargs -0 -n 1 process_one; do
find ../www/scripts/lib/katex -name '*.js' | while read file; do

	# check to make sure it's not already wrapped?  if so, continue

	cat wrapbegin.txt $file wrapend.txt > wrapfile.js && # we can't immediately overwrite the file while we're reading it!

	mv wrapfile.js $file && # but now we can, since previous && guarantees we have successfully *completed* the previous command.

done &&

rm wrapbegin.txt wrapend.txt &&

echo 'done.'

