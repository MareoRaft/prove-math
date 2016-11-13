This directory contains things to prepare our website for consumption.
In particular, SASS files need to be built into CSS files, and JS6 files need to be built into JS5 files.

The MAIN file that takes care of building things is gulpfile.js, and it is located in the PARENT DIRECTORY of this directory.  Start by looking at that file.

r.js is our JS minifier and optimizer, which we use on the server before releasing website to the public.
rbuild.js is config options used by r.js
