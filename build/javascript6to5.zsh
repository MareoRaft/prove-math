# this doesn't seem to work on BSD :(((((
for path_end in www/scripts6/lib/*(e*'REPLY=${REPLY#www/scripts6/}'*) main.js config.js ; do
	babel www/scripts6/$path_end > www/scripts/$path_end &
done
wait
# see also, xargs! http://unix.stackexchange.com/questions/35416/four-tasks-in-parallel-how-do-i-do-that
