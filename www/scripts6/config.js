// THIS FILE ITSELF IS NOT CACHE BUSTED
require.config({
	urlArgs: "bust=" + (new Date()).getTime(),
	baseUrl: "scripts/lib", // the default base is the directory of the INDEX.HTML file
	paths: { // other paths we want to access
		jquery: "http://code.jquery.com/jquery-1.11.2.min",
		underscore: "https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.2/underscore-min",
		d3: "d3-for-development", // if we add patches separately, then we can just use https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min
		katex: "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.3.0/katex.min", // or 0.2.0
		mathjax: "http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML&amp;delayStartupUntil=configured",
		// marked: "https://cdnjs.cloudflare.com/ajax/libs/marked/0.3.2/marked.min", // disabled for consistent development
		chosen: "https://cdnjs.cloudflare.com/ajax/libs/chosen/1.4.2/chosen.jquery.min",
		jsnetworkx: "https://raw.githubusercontent.com/fkling/JSNetworkX/v0.3.4/jsnetworkx", //actually we maybe should download this
		main: "../main",
	},
	shim: { // allows us to bind variables to global (with exports) and show dependencies without using define()
		underscore: { exports: "_" },
		chosen: { deps: ["jquery"] },
		mathjax: {
			exports: "MathJax",
			init: function (){
				MathJax.Hub.Config({
					tex2jax: {
						inlineMath: [['$','$'], ['\\(','\\)']],
						processEscapes: true, // this causes \$ to output as $ outside of latex (as well as \\ to \, and maybe more...)
					},
				});
				MathJax.Hub.Startup.onload();
				return MathJax;
			}
		},
	},
})

require(["main"], function(main){
	// pass.  by loading main, we run main.js
})
