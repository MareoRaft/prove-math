1. a "review" mode which is like a QuizUp quiz.  It quizzes you on things you know, in such a way as to not be redundant. (won't repeat anything, won't repeat things too closely related (depending on settings you set)).

The quiz and the program itself may have some sort of positive feedback feature (points, stars, or whatnot), since that seems to motivate ppl on KA and SO.

The quiz will REMEMBER what it has quizzed you on in the past, so that it can TARGET the things you may be forgetting, and leave alone the things you have recently visited!
2. the ability for users to find other users who have similar skills or "complementing" skills (for the purpose of collaboration).
4. API for people to request nodes in the form of json dictionaries
5. Zero is a natural number
6. Analysis and real analysis are separate topics that may be linked at some point
7. definitions names should be lowercase (unless someone's name, etc) and underlined as the appear ON THE NODE NAMES in the DAG view.  definitions should be automatically generated from the dunderlines when the name attribute is missing.
8. comments allowed on nodes.
9. make SVG nodes refresh so that they are ontop of links again (maybe when making new links, refresh the sources and targets as opposed to refreshing ALL nodes)  use this if it helps: d3.selection.prototype.moveToFront = function() { return this.each(function() { this.parentNode.appendChild(this); }); }; And then you can say selection.moveToFront()
source: http://stackoverflow.com/questions/14167863/how-can-i-bring-a-circle-to-the-front-with-d3
10. we can give definitions WEIGHTS depending on how many things are dependent on them!  Or even better,  definitions can be given a weight based on how much of a payoff they are to YOU.  Maybe not.  That's what the cloud is supposed to do.  Okay, a static weight based on how many things use them.
11. add some window.onerror thing to JS which will tell me which assertion failed in check-types
12. RESTRICTIONS.  thms written in generality, but then users apply restrictions.  For example, thrm is true for multigraphs, but user is only concerned with simple graphs.  With the restriction, the node will appear as a statement about simple graphs. (but implementing this would probably require thrms to be written in an unambiguous logical language.  that way, it is possible to parse the thrm and find the REQUIREMENTS and check each one against the RESTRICTION.  this is definitely worth doing, but will take a very long time to do!)
13. optional setting --> see a definition when you hover over the node.
14. use a class attribute max_importance and min_importance instead of overriding the setter in node.py
15. we need to learn how to migrate our mongo database.  In the future we will eventually have to move servers, and when we do, we don't want to be sitting there with an "unmovable" mongo database.
16. Instead of writing in the dependencies ourselves, we want the program to search through the description and label each word as an ENGLISH word or a DEPENDENT word, then search through names and their plurals to populate the dependencies.
17. use refs for a possible speed boost in the future (NetworkX holds refs. then we don't have to find nodes by id later on.  code: class ref:def __init__(self,obj):self.obj = objdef get(self):return self.objdef set(self,obj):self.obj = obj
