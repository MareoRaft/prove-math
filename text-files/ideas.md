1. a "review" mode which is like a QuizUp quiz.  It quizzes you on things you know, in such a way as to not be redundant. (won't repeat anything, won't repeat things too closely related (depending on settings you set)).

The quiz and the program itself may have some sort of positive feedback feature (points, stars, or whatnot), since that seems to motivate ppl on KA and SO.

The quiz will REMEMBER what it has quizzed you on in the past, so that it can TARGET the things you may be forgetting, and leave alone the things you have recently visited!
2. the ability for users to find other users who have similar skills or "complementing" skills (for the purpose of collaboration).
6. Analysis and real analysis are separate topics that may be linked at some point
8. comments allowed on nodes.
9. make SVG nodes refresh so that they are ontop of links again (maybe when making new links, refresh the sources and targets as opposed to refreshing ALL nodes)  use this if it helps: d3.selection.prototype.moveToFront = function() { return this.each(function() { this.parentNode.appendChild(this); }); }; And then you can say selection.moveToFront()
source: http://stackoverflow.com/questions/14167863/how-can-i-bring-a-circle-to-the-front-with-d3
10. we can give definitions WEIGHTS depending on how many things are dependent on them!  Or even better,  definitions can be given a weight based on how much of a payoff they are to YOU.  Maybe not.  That's what the cloud is supposed to do.  Okay, a static weight based on how many things use them.
12. RESTRICTIONS.  thms written in generality, but then users apply restrictions.  For example, thrm is true for multigraphs, but user is only concerned with simple graphs.  With the restriction, the node will appear as a statement about simple graphs. (but implementing this would probably require thrms to be written in an unambiguous logical language.  that way, it is possible to parse the thrm and find the REQUIREMENTS and check each one against the RESTRICTION.  this is definitely worth doing, but will take a very long time to do!)
14. use a class attribute max_importance and min_importance instead of overriding the setter in node.py
15. we need to learn how to migrate our mongo database.  In the future we will eventually have to move servers, and when we do, we don't want to be sitting there with an "unmovable" mongo database.
16. Instead of writing in the dependencies ourselves, we want the program to search through the description and label each word as an ENGLISH word or a DEPENDENT word, then search through names and their plurals to populate the dependencies.
17. use refs for a possible speed boost in the future (NetworkX holds refs. then we don't have to find nodes by id later on.  code: class ref:def __init__(self,obj):self.obj = objdef get(self):return self.objdef set(self,obj):self.obj = obj
18. ways to optimize graph spacing: http://stackoverflow.com/questions/15076157/optimizing-charge-linkdistance-and-gravity-in-d3-force-directed-layouts
19. about betweenness centrality: http://glowingpython.blogspot.com/2013/02/betweenness-centrality.html
20. give nodes some approximate start position based on sourciness sinkiness.  This will order things nicer AND stop stuff from exploding on load
21. ADD support for Ali's "intuition" within proofs.
22. add support for expandable bubbles within proofs.
23. How do we tell users "check out this chapter of this book" to learn more about a theorem or to get exercises for the theorem.
24. create preview to convert Markdown + LaTeX dropin so we can see stuff.
25. implememt nicknames
26. if context dependent definitions share the same name and are within 8 (CUSTOMIZABLE. anywhere from 1 to infinity) edges from eachother, then show the context on the DAG.
28. consider https://oauth.io/home
29. for JSON, implemen id's to get a specific node.  in the future, add "search" function where you can put a name it guesses what you want.
31. check that everything works in all browsers --> check!  except for Internet Explorer...
32. change nodes array to a dictionary. that way we can find nodes by ID QUICKLY
33. to finish off the editable thing to work... ALL keys should have ARRAYS as values.  Or so it seems..... this would be simpler to work with.  But consider that we may need to call node.name[0] elsewhere in the code.  Otherwise, we could just build a logic to handle that..
34. implement a "tag" system for dependencies and proof "types".  See if there is a library out there for this!  I like this library: http://harvesthq.github.io/chosen/  .  Also this one . http://sean.is/poppin/tags  .  And this one!! https://maxfavilli.com/jquery-tag-manager    .   There are many many more.
35. add in mathjax rendering for html.  is there a mathjax function i can call?
36. fix window resizing on resizing
37. just keep building javascript features!  do chosen.  anything!
39. consider switching everything to flex instead of block.  This (should (you need to test this before doing anything)) mean that things resize automatically as you resize the browser window.
40. pushArray causing issue with for in loop javascript.
42. for algebra things, if they HAVE NOT learned abt structure, define a field (for example) to have each property (pull them out).  If they HAVE learned, then it's a commutative division ring.
43. Users can select what fields they already know and level of familiarity and it pre-highlight nodes for learned

27. use the premade https://github.com/kerzol/markdown-mathjax thingy to do conversion.  Instead of building our own markdown mathjax stuff. (But we would still need to consider running conversion on the server for speed boosts.  and would that still work with this integration?)  I think the dev makes the right decision to FIRST apply MathJax and SECOND apply Markdown.  We should do the same.  Also he uses the "marked" markdown parser, which claims it is built for speed.  Sounds good.  It's in JavaScript, which means client-side. (as opposed to our current one which is on server side).  It seems that KA uses a version of marked.js too (https://github.com/Khan/simple-markdown).  Maybe it's a good choice!

44. understand how https://github.com/kerzol/markdown-mathjax/blob/master/editor.html works.  either USE it, or EMULATE it
45. Understand what MathML is.  perhaps make a mathjax config with a \big{} that does nothing, so that blind people can hear \big and have capital letters distinguished from lowercase.
46. https://groups.google.com/forum/#!topic/rubyonrails-talk/STny0vF5FX4 -- this is a discussion on embedding JSON into an HTML page.  I think the json encoding is good enough, and because JSON is supposed to be a subset of javascript, that we will have no issue.  but just in case, there's the link.
49. It looks like Tornado offers builtin oauth things: http://www.tornadoweb.org/en/stable/auth.html#module-tornado.auth
Victoria Feedback
-----------------------
51. the "hover" definitions on the graph-animation are not rendered!
53. refresh error. (when i reload, it breaks) --> Andrew adds back and forward browser button things.
53.5 can we remember when somebody is already logged in?
Continued
--------------
54. consider using https://github.com/ftlabs/fastclick to make clicking not laggy on mobile devices, only if needed.
57. need stopPropogation or preventDefault or something to disable drag on firefox after clicking node.
Andrew stuff
------------------
58. restrict the nodes to the visible screen -- can we have a repulsive force along the boundary?
59. some reaction to pressing "I learned it"
60. deal with rogue empty plurals.  what have i done!!!
61. create vertical centering for key and value-block if possible.
62. after next push to server, check all cookie and oauth things to make sure they work right.