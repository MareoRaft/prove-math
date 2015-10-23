suggested use:

py.test --capture=no --maxfail=1 path/to/file.py

...and then when you need to debug, use:

py.test --capture=no --maxfail=1 --pdb path/to/file.py




test everything in current directory and all children:

py.test




test one file:

py.test path/to/file.py




useful options:

-x, --exitfirst       exit instantly on first error or failed test.
  --maxfail=num         exit after first num failures or errors.

  --capture=method      per-test capturing method: one of fd|sys|no. # THIS MEANS print() statements in code will go through!
  -s                    shortcut for --capture=no.

--pdb                 start the interactive Python debugger on errors.

-v, --verbose         increase verbosity.