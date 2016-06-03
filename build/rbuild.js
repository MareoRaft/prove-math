/*
options for r.js

for legacy purposes, the STANDALONE command that did this same functionality was:
node build/r.js -o mainConfigFile=www/scripts/main.js baseUrl=www/scripts/lib name=../main out=www/scripts/main-optimized.min.js generateSourceMap=true preserveLicenseComments=false optimize=uglify2
*/
({
	mainConfigFile: "../www/scripts/config.js",
	baseUrl: "../www/scripts/lib",
	name: "../config",
	out: "../www/scripts/config-optimized.min.js",

	generateSourceMap: true,
	preserveLicenseComments: false, // this is necessary for generateSourceMap to work
	optimize: "uglify", // uglify is the default, which now uses uglify2 automatically

	// removeCombined: true,
	// findNestedDependencies: true,

	paths: {
		// https://github.com/jrburke/requirejs/issues/791
		// http://www.anthb.com/2014/07/04/optimising-requirejs-with-cdn-fallback
		jquery: "jquery-min",
		underscore: "underscore-min",
		d3: "d3-for-development",
		katex: "katex-min",
		mathjax: "http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML&amp;delayStartupUntil=configured",
		marked: "marked",
		chosen: "chosen-min",
		jsnetworkx: "jsnetworkx-min",
		main: "../main",
	},
})
