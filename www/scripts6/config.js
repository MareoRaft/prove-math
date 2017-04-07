// THIS FILE ITSELF IS NOT CACHE BUSTED
require.config({
	urlArgs: "bust=" + (new Date()).getTime(),
	baseUrl: "scripts/lib", // the default base is the directory of the INDEX.HTML file
	paths: { // other paths we want to access
		// keep in mind that the local and remote URLS are NOT necessarily the SAME VERSION of the library.  :(  because i'm lazy.  but no issues so far.
		// IF THINGS CONTINUE TO BE SLOW: try www.jsdelivr.com CDN.
		jquery: [
			"jquery-min",
			"http://code.jquery.com/jquery-1.11.2.min", "https://cdn.jsdelivr.net/jquery/2.2.4/jquery.min"
		],
		underscore: [
			"underscore-min",
			"https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.2/underscore-min",
			"https://cdn.jsdelivr.net/underscorejs/1.8.3/underscore-min"
		],
		d3: "d3-for-development", // if we add patches separately, then we can just use https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min, https://cdn.jsdelivr.net/d3js/3.5.17/d3.min
		// katex: [
		// 	"katex-min",
		// 	// "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.3.0/katex.min",
		// 	"https://cdn.jsdelivr.net/katex/0.6.0/katex.min"
		// ], // or 0.2.0
		mathjax: [
			"https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML&amp;delayStartupUntil=configured",
			// "https://cdn.jsdelivr.net/mathjax/2.1/MathJax.js?config=TeX-AMS_HTML&amp;delayStartupUntil=configured", // no longer works.  don't know why.
			// "mathjax-min-2.7.0.js?config=TeX-AMS_HTML&amp;delayStartupUntil=configured", // we also placed MathMenu and MathZoom in the extensions folder, since mathjax depends on these. // no longer working. don't know why.
		],
		marked: [
			"marked",
			"https://cdnjs.cloudflare.com/ajax/libs/marked/0.3.2/marked.min",
			"https://cdn.jsdelivr.net/marked/0.3.5/marked.min"
		],
		mousetrap: [
			"mousetrap.min",
			// "https://cdnjs.cloudflare.com/ajax/libs/mousetrap/1.6.0/mousetrap.min",
		],
		chosen: [
			"chosen-min",
			"https://cdnjs.cloudflare.com/ajax/libs/chosen/1.4.2/chosen.jquery.min",
			"https://cdn.jsdelivr.net/chosen/1.1.0/chosen.jquery.min"
		],
		jsnetworkx: [
			"jsnetworkx-min",
			"https://raw.githubusercontent.com/fkling/JSNetworkX/v0.3.4/jsnetworkx"
		],
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
			},
		},
	},
})

require(["main"], function(main){
	// pass.  by loading main, we run main.js
})
