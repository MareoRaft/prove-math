.. info about git tagging can be found here!: https://git-scm.com/book/en/v2/Git-Basics-Tagging

Change Log
=========================
All notable changes to ProveMath will be documented in this file.
This project attempts to follow the principles of http://keepachangelog.com as closely as possible.





Version [1.2.0]
----------------------
2016-06-07 | `commit <https://github.com/ProveMath/prove-math/commit/1b5de0b9286e388379b0526e6824f7c34ba2642d>`_ | `diff <https://github.com/ProveMath/prove-math/compare/v1.1.0...v1.2.0>`_

Added
~~~~~~~~
  * Many user preferences added.  Those and other global options relocated to the new config.py file.
  * newest graph methods (like choose_goal and most_important) organized into PMDAG and MathGraph classes.  PMDAG is like DAG but with our custom node object involved (add_n and most_important).  MathGraph is like a wrapper around PMDAG that makes convenient methods that take in our user object as input and output what the user needs.
  * nodes_to_send, in MathGraph, uses the user's preferences to automatically choose what to send to the user in all situations.
  * User can now click button to get goal and pregoal suggestions!
  * documentation created with Sphinx.  It can be viewed at http://provemath.org/docs (or localhost/docs during development).
  * Classes like Vote, Votable, Atom, and Curriculum have been created.  But none of them are in use yet.

Changed
~~~~~~~~~~
  * build.sh file and watchers replaced by gulpfile.js.  With the new gulp build system, things are simpler and more cross-platform compatible.
  * autoprefixer_ now runs after compass, and all vendor prefixes have been removed from our SCSS code.









Version [1.1.0]
---------------------
2016-04-24 | `commit <https://github.com/ProveMath/prove-math/commit/c77b746168ab26e6dae3bc7d012e8c13b4b8caee>`_ | `diff <https://github.com/ProveMath/prove-math/compare/v1.0.0...v1.1.0>`_

Added
~~~~~~~~
  * user_learn_suggestion method to DAG (it will later be renamed choose_pregoals and choose_goal).  This method is the culmination of many methods and flexibility added to the networkx classes.  Now users can receive a deep goal node and then learn towards it.
  * Users can click to start a new subject, and receive the starting nodes for that subject.
  * basic logging

Fixed
~~~~~~~
  * Cookies now hold only the user identifier (oauth account type and ID)
  * NOT LOGGED IN users can now interact with the website in full, just like logged-in users.









Version [1.0.0]
---------------------
2016-01-23 | `commit <https://github.com/ProveMath/prove-math/commit/160d0f5e02a09650a9a19517a0d4b247f555db36>`_ | `diff <https://github.com/ProveMath/prove-math/compare/v0.5.0...v1.0.0>`_

Added
~~~~~~~~
  * User actions (prefs, learning and unlearning nodes) auto-save to MongoDB
  * Users can logout, and cookies allow users to remain logged in for longer.
  * New and edited nodes can be saved from the browser to MongoDB.
  * category theory content started
  * A search bar that searches MongoDB text index and returns the best-matching nodes.
  * Users can add and remove dependencies/links from the graph.

Changes
~~~~~~~~~~
  * Source nodes (called "axioms" at the time) now get created in MongoDB during the pre-json_to_mongo process.  This is a BREAKING change, and it's easiest to rebuild the whole MongoDB "nodes" collection from scratch using the .pre-json files.
  * "learn mode" created.  Users see what they've learned and what they are capable of learning.  Graph expands as user learns more.  (previously, the user saw a certain radius around some starting node)

Fixed
~~~~~~~~
  * Graph growing glitch fixed.  Yep.  That was annoying.






Version [0.5.0]
------------------------
2015-10-28 | `commit <https://github.com/ProveMath/prove-math/commit/a634de5b044a34291a9dd6e5a2bffa25541f5e24>`_ | `diff <https://github.com/ProveMath/prove-math/compare/v0.4.0...v0.5.0>`_

Added
~~~~~~~~
  * compass_ watch for auto conversion of SCSS files to CSS
  * babel_ watchdog for auto transpilation of JS 6 files to JS 5
  * blinds.js file to display dictionaries (currently, just nodes) in browser
  * User class to save user info in MongoDB
  * chosen_ third party library for drop-down menus
  * oauth login (see auth.py, main.py, and the 'login' section of index.html)
  * 'command' system to organize websocker communication



Changed
~~~~~~~~~~~
  * combinatorics and graph theory content finished







Version [0.4.0]
---------------------------
2015-08-20 | `commit <https://github.com/ProveMath/prove-math/commit/c3ba5207bef3650e23852700f7a3b350196c8114>`_ | `diff <https://github.com/ProveMath/prove-math/compare/v0.3.0...v0.4.0>`_

Added
~~~~~~~~~
  * pymongo experimenting
  * .pre-json to .json conversion
  * combinatorics content!
  * a .gitignore
  * Mongo class (wrapper around pymongo)
  * d3 SVG graph animation
  * Lots of JS
  * graph theory content up to HW 14
  * We can now take dictionaries from MongoDB_, create Node objects from them, create a DAG, and send it to the client.

Changed
~~~~~~~~~~
  * "node" class to "Node" class
  * Reorganized folder structure of project.  There is now a "server" folder that contains "lib" for code and "data" for content.

Fixed
~~~~~~~~~
  * path convention for imports

Removed
~~~~~~~~~~
  * Experimental files






Version [0.3.0]
----------------------
2015-06-14 | `commit <https://github.com/ProveMath/prove-math/commit/a76021826234b67a7bed25114da040b035924d4e>`_ | `diff <https://github.com/ProveMath/prove-math/compare/v0.2.0...v0.3.0>`_

Added
~~~~~~~
  * more functionality for Graph, DiGraph, and DAG, with tests.
  * pytest
  * Markdown_ perl file.
  * Idea for JSON support
  * global graph object exports to a dictionary, gets converted to a JSON string, and successfully sent to the client through a websocket

Fixed
~~~~~~~
  * monkeypatching for networkx.DiGraph




Version [0.2.0]
---------------------
2015-10-06 | `commit <https://github.com/ProveMath/prove-math/commit/ead16af77ecfedc7c6201bfebb5cba936a64e45e>`_ | `diff <https://github.com/ProveMath/prove-math/compare/v0.1.0...v0.2.0>`_

Added
~~~~~~~~
  * networkx_ graph library...
  * monkeypatched the networkx classes Graph and DiGraph
  * attached the class DAG (Directed Acyclic Graph) to networkx.




Version [0.1.0]
---------------------
2015-05-13 | `commit <https://github.com/ProveMath/prove-math/commit/00fc9618c73b365da71340cec976253354890183>`_ | `diff <https://github.com/ProveMath/prove-math/compare/v0.0.1...v0.1.0>`_

..	well i wanted to compare to version 0 (that is, NOTHING at all), but I don't know how.  So I tagged the initial commit as v0.0.1 instead

Added
~~~~~~~~~~~~~
  * Brainstorms for MathJax, KaTeX, domain names, and graph animation
  * List of contacts/people for the project
  * Experiments with d3 and networkx
  * custom node class
  * tornado webserver
  * index.html file
  * SCSS files (see sass folder)
  * main.js file
  * check-types third party type-checking JS library
  * requireJS
  * LICENSE and README



..	_markdown: http://daringfireball.net/projects/markdown/
..	_networkx: http://networkx.readthedocs.io/en/latest/#
..	_compass: http://compass-style.org
..	_babel: https://babeljs.io
..	_chosen: https://harvesthq.github.io/chosen/
..	_mongodb: https://www.mongodb.com
..	_autoprefixer: https://github.com/postcss/autoprefixer
