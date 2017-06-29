Installation
================

If you are a provemath developer, there are a number of tools you may need to install.  Below is a list of tools and how to install them.  MongoDB is not included here, as it has it's own page the Programmers section.  It's always a good idea to check if a tool is already installed on your computer before spending time trying to install it.



..	_install-brew:

Homebrew
------------
Homebrew (or *brew*, for short) is a package manager for Macs.  It is installed with the command::

	/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

If you wish, you may read more about brew_.

..	_brew: http://brew.sh




..	_install-ruby:

Ruby
------------
Below is a method for installing ruby using the *brew* package manager.  If you don't have a package manager, then you should first :ref:`install brew <install-brew>`.

Use brew to install ruby::

	brew install ruby

You can confirm it's installed by running::

	brew info ruby

That's it!




..	_install-gem:

RubyGems
--------------
Note: You must have :ref:`ruby installed <install-ruby>` before installing rubygems.

If you installed ruby using brew, then rubygems should already be installed!  Woohoo!

You can confirm installation and view the version of rubygems (called `gem`) on the command line::

	gem -v

There is an alternative method for installing rubygems_.

..	_rubygems: https://rubygems.org/pages/download




..	_install-sass:

SASS
-----------
Note: You must have :ref:`ruby gems installed <install-gem>` before you can install sass.

Sass is a ruby gem, so update your ruby gem system::

	gem update --system

Then install the sass gem::

	gem install sass

You can confirm that it's installed by checking the version::

	sass -v

Sass_ has a really great website.  You can find more info there.

..	_Sass: http://sass-lang.com





..	_install-compass:

Compass
-----------------
Note: You must :ref:`install sass <install-sass>` before you can use compass.

Then install compass, which gives some extra features, like the ability to run a daemon that sniffs for changed scss files and automatically updates them to css in the background::

	gem install compass

You can confirm it's installed by running the command::

	gem list | grep compass

There is a compass_ website with install information.

..	_compass: http://compass-style.org/install/






..	_install-node:

Node
-------------
Node_ is a language nearly identical to JavaScript that can be run outside of a browser.  It is popular among web developers because it basically allows them to write in the same language on the server side and the client side.

You can install it with your computer's package manager::

	brew install node

It is a whole language, so it may have a number of dependencies :)  Here is an `alternative installation`__.

__ node-install-site_
..	_node-install-site: https://nodejs.org/en/download/
..	_Node: https://nodejs.org

After installing node, you can install gulp and other dependencies:

Gulp
~~~~~
npm install gulp-cli -g
npm install gulp -D

Gulp dependencies
~~~~~~~~~~~~~~~~~~~~~~
npm install dependency-name





..	_install-npm:

npm
------------
npm is the official node package manager.  Therefore, make sure you have :ref:`node installed <install-node>`.

npm should come automatically installed when you install node.  Alright!

You can confirm installation and view the version of npm on the command line::

	npm -v

There is a manual method for installing npm_.

..	_npm: http://jason.pureconcepts.net/2011/12/installing-node-js-npm-redis-mac-os-x/









..	_install-babel:

Babel
--------------
We use babel to convert our JavaScript 6 (a.k.a. JS Harmony, a.k.a. ECMA Script 6) files to JavaScript 5 files.  In a year or two when browsers fully support JS 6, we won't need this anymore.

Our JS6 files are stored in ``www/scripts6`` and our JS5 files are stored in ``www/scripts``.  For any JS5 file that has a corresponding JS6 files, MAKE SURE to always edit the JS6 file, not the 5 file.  The 5 file is automatically overwritten by babel every time the JS6 file is updated.

Recommended installation:  First :ref:`install npm <install-npm>` on your system.  Then::

	npm install --save-dev babel-cli

I haven't figured out the kinks, because it seems a new version of babel was released.  Can somebody figure out the new usage?  We might migrate to a Grunt build system in the future :).  Official babel_ website installation.

There is also a pybabeljs_ library which is an alternative way of running babel through python.

..	_babel: https://babeljs.io/docs/setup/#installation
..	_pybabeljs: https://github.com/MareoRaft/babeljs-python/tree/master/babeljs



