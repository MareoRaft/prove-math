# provemath.org
It's an add venture!
The next generation of math education ;-)

I think this will be very engaging for people interested in programming or math, since it poses a number of challenges.  Contributors *can* put this on their resume.  Students can do this as an independent study (if we get approval), but you must let me know ahead of time.


Project description below!
------------------------------
We are building a website for people to learn math.  Math is made from initial "definitions" and "axioms", and then "theorems" that follow.  Imagine that each definition is represented by a node.  When a *new* theorem is proved based on a few definitions/theorems, we draw arrows from those definitions/theorems to the *new* theorem (which is also a node).

The result will be a big hierarchy of different math theorems!  That is, a directed acyclic graph (DAG).

The cool thing is that users can see this hierarchy.  They can navigate to each node and learn the theorem, get an explanation, read proofs (or attempt to do it themselves).  In the future I intend for this content to be user contributed, using a Reddit/SO upvote system.

As a learner, you visit the website, and as you learn a node, check it off. It turns green. As you learn more nodes, nodes nearby to what you know appear. This is the "cloud" of things within your reach of learning.

There will be some advanced algorithms, etc, to decide what new nodes to send to a user from the server.

There are interesting results of this setup. One example is that a person is learning two different math fields such as matrix theory and combinatorics. The server would find nodes connected to both disciplines and help the user to bridge the two together.

Another example is that a user can select a high level theorem and receive the ancestor tree, that is, the concepts they must know to build up to the high level theorem. This feature would be useful for a professor who wishes to design a course for his students. He can even share the course online, etc.


Programming to make this work
------------------------------------
  * We need a database to store the giant math DAG (MongoDB).
  * We have a virtual server on DigitalOcean.
  * Python on the server-side grabs info from the DB, processes it with NetworkX library, and serves it with Tornado Web Server.
  * Javascript on the client side w/ jQuery, JSNetworkX, bundled together with RequireJS.  We are using LaTeX for math typesetting and MathJax to render it.
  * We have a GitHub at https://github.com/ProveMath/prove-math

Credits
------------
  - Matthew Lancellotti - contributor
  - Theodore Siu - Python contributor
  - Greg Mattson - Python NetworkX contributor
  - Tim Naumovitz - The combinatorics material is based on his lectures

Copyright 
--------------
© provemath.org 2015
