Discussion Links
==================
http://meta.math.stackexchange.com/questions/16809/a-mathjax-alternative-from-khan-academy
http://aperiodical.com/2014/09/katex-the-fastest-math-typesetting-library-for-the-web/


MathJax server-side
========================
https://github.com/mathjax/MathJax-node

this project renders the mathjax on the server's side and sends over the HTML.  This is the same thing that KaTeX does to gain speed.




MathJax
===========
supports everything.  not as pretty as KaTeX.  May have SLOW side-effect.

here is how you set up, with MathML preference and stuff:
http://docs.mathjax.org/en/latest/start.html




KaTeX
========
Pros: KA actually runs KaTeX first and then for anything that can't be rendered, MathJax!  This is actually very nice.  Benefits without the bad stuff! The following link shows how you use a plain old try and catch to do it:
https://github.com/Khan/KaTeX/issues/186
go direct to the source!  THIS is how you do it:
https://github.com/Khan/KaTeX#usage

ommitting the baseUrl in require.config object makes all path interpretations relative!

What's missing from KaTeX?

\mapsto
\longrightarrow
\longmapsto

matrices

piecewise function definitions

n \choose k

nth root

\sim  (supposedly) arrays and eq alignments not supported






Conclusion (thus far)
========================
Since we plan to support all sorts of math, we really need MathJax's wide support.  We should start w/ MathJax and then look into performance improvements through server-side rendering or KaTeX add-on in the future.
