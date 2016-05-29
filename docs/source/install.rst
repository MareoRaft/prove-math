Installation
================

If you are a provemath developer, there are a number of tools you may need to install.  Below is a list of tools and how to install them.  It's always a good idea to check if a tool is already installed on your computer before spending time trying to install it.




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


