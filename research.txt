Javascript Network Library
===========================

Crow
----
Crow is a collection of graph-traversal and pathfinding libraries. It includes algorithms such as breadth-first search, Dijkstra's algorithm, and A*.
https://github.com/nanodeath/CrowLib



JSNetworkX
-----------
is a port of NetworkX for JS!!
https://github.com/fkling/JSNetworkX



graph library function JS
------------------------

CYTOSCAPE
http://js.cytoscape.org
this seems to have all useful functions, but when i look for "parents" does this weird compound nodes thing.  I don't want compound nodes.  I want regular DiGraph stuff.



visual graph stuff Javascript
-----------------------------

consider arbor again!  for front end graph organization, but not drawing!

THE BIG 3 CANDIDATES ARE ARBORJS, FLARE, AND D3:  NEW ONE IS SIGMAJS

SIGMAJS
http://sigmajs.org
uses WebGL when the browser supports it!!!
customizable!
made for graph drawing only.


http://arborjs.org
pros: capable, pick your own front end, jQuery, force-directed layout
you can edit friction, repulsion, etc. http://arborjs.org/halfviz/#/case-of-the-silk-king
cons: you must do front end yourself, text a little blurry when you browser-zoom-in
line weights don't seem to work
when nodes get bigger, they are only bigger visually, so they will overlap each other if too big --> this could be a dealbreaker --> it seems you CAN change size via arbor but we must verify
{color:"#00ff00", radius:1}
sys.tweenNode(myNode, 3, {color:"cyan", radius:4})
tweenNode is a transition animation, over 3 seconds.
i sent an email about forcing the y coordinate to be 0 but allowing everythig else to flow.  The response is important, also it seems important to have some level of support from them.


http://flare.prefuse.org/demo
pros: very capable
cons: has more than just graphs, seems no longer under development!  Somebody claims flare was a predecessor of D3!

D3
----
cola is a drop in replacedment for d3 force layout!  it's worth a try in the future to see if it's any nicer...
http://marvl.infotech.monash.edu/webcola/
-------
https://github.com/mbostock/d3
http://bl.ocks.org/mbostock/4062045
pros: SVG, javascript, works great, very robust
cons: extraneous things
http://bost.ocks.org/mike/
plot.ly  is built on d3
here is how to force some things!:
http://bl.ocks.org/mbostock/3750558



OTHERS:

http://stackoverflow.com/questions/7034/graph-visualization-library-in-javascript
has links to other resources!

https://www.nodebox.net/code/index.php/Graphing
pros: uses the Boost Graph Library for Python, very mature
cons: doens't appear interactive (not sure)

Boost Graph Library
pros: mature

Protovis
http://mbostock.github.io/protovis/ex/force.html
pros: uses a force-directed layout, interactive!, can adjust node size according to weights, uses SVG
cons: a whole bunch of extraneous stuff, no longer being developed, new project-->D3.js
http://www.graphdracula.net
pros: JS, SVG, Raphael, simple to use
cons: may not be highly customizable, i don't know how good autopositioning is
has links to other resources!

- yFiles for HTML -
pros: commercial
cons: need company email to try it



http://www.graphviz.org/About.php
pros: very capable
cons: no animation!

http://js-graph-it.sourceforge.net/index.html
pros: small project, little to no javascript
cons: ditto!  i don't think it's very capable.

http://jsplumb.org/doc/home.html
cons: demo kindof meh

https://github.com/jackrusher/jssvggraph
pros: works very nice
cons: doesn't appear interactive


http://labs.unwieldy.net/moowheel/
pros: looks very professional
cons: seems to be only for representing graphs in a wheel (circle) format





how graph spacing works
-----------------------
http://arborjs.org/docs/barnes-hut








Personal Domain Email Accounts
==============================
#
http://howto.ccs.neu.edu/howto/mail/configuring-alpine/

zoho offers 10 free addresses!
After an hour or two, log in to your Zoho Mail Control Panel and click Verify
verified!
working!

RoundCube
https://roundcube.net/download/
roundcube is free but you may have to install stuff on your server.
roundcube sounds very good and we may use it in the future when we expand.


