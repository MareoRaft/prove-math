"use strict";

// require and requirejs are two names for the same function.  when require gets {} input, it basically calls require.config for you
require.config({
	// by eliminating baseUrl, everything becomes relative, which is the convention that KaTeX files follow.
	// in order for this to work, we CANT USE PATHS SHORTCUTS FOR directories either
	// now i'm trying KaTeX by CDN instead.
	baseUrl: "scripts/lib", // the default base is the directory of the INDEX.HTML file
	paths: { // other paths we want to access
		jquery: "http://code.jquery.com/jquery-1.11.2.min", // and the .js is added like always by require
		underscore: "https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.2/underscore-min",
		// backbone: "https://cdnjs.cloudflare.com/ajax/libs/backbone.js/1.1.2/backbone-min",
		d3: "https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min",
		katex: "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.3.0/katex.min", // or 0.2.0
		mathjax: "http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML&amp;delayStartupUntil=configured" },
	shim: { // allows us to bind variables to global (with exports) and show dependencies without using define()
		underscore: { exports: "_" },
		// backbone: { deps: ["jquery", "underscore"], exports: "Backbone" },
		mathjax: {
			exports: "MathJax",
			init: function init() {
				MathJax.Hub.Config({
					tex2jax: { inlineMath: [["$", "$"]] } });
				MathJax.Hub.Startup.onload();
				return MathJax;
			}
		} } });

require(["jquery", "underscore", "d3", "browser-detect", "check-types", "katex", "mathjax", "profile"], function ($, _, d3, browser, check, katex, mathjax, undefined) {

	// websocket stuff!
	var ws = "WebSocket" in window ? new WebSocket("ws://54.174.141.44:7766/websocket") : undefined; // url to send websocket messages
	if (!def(ws)) {
		die("Your browser does not support websockets, which are essential for this program.");
	}

	$(".math").each(function () {
		// this is set up as client-side rendering.  see #usage above and use katex.renderToString for server side.
		var texText = $(this).text();
		var el = $(this).get(0);
		var addDisplay = "";
		if (el.tagName === "DIV") {
			addDisplay = "\\displaystyle";
		}
		try {
			katex.render(addDisplay + texText, el);
		} catch (err) {
			if (err.__proto__ === katex.ParseError.prototype) {
				$(this).html("$" + texText + "$");
			} else {
				$(this).html("<span class='err'>" + "Hi! " + err + "</span>");
			}
		}
	});

	ws.onopen = function () {
		ws.send("Hello, world");
	};
	ws.onmessage = function (evt) {
		alert(evt.data);
	};

	var a = ["hi", "there"];
	check.array(a);
	check.iterable(a);
	// check.array.of.string(a) // not yet working

	$("section").click(function () {
		alert("jquery");
	}); // jquery is smart to team up with require and include .ready() builtin, so we no longer need that wrapper around everything

	// setup all the things we can do before actually getting the data:

	function me(node) {
		alert("me!");
		return true;
	}

	function randColor(node) {
		return "rgb(" + node.x + ", 0, 0)";
	}

	function dragstart(node) {
		d3.select(this).classed("fixed", node.fixed = true);
	}

	function dblclick(node) {
		d3.select(this).classed("fixed", node.fixed = false);
	}

	var width = $("body").width(),
	    height = $(window).height();

	var force = d3.layout.force().size([width, height]).charge(-200).linkDistance(40).on("tick", tick);

	var drag = force.drag() // perhaps this is a frictional force?  drag? which wouldn't exist until we say drag()
	.on("dragstart", dragstart);

	var svg = d3.select("body").append("svg").attr({
		width: width,
		height: height });

	// unfortunately marker inherits its stroke and fill from the parent, and this is the only way to control that
	svg.append("defs").attr("fill", "green").selectAll("marker").data(["arrow-head"]) // binding 'arrow-head' is our way of attaching a name!
	.enter().append("marker").classed("arrow-head", true).attr({
		id: String,
		viewBox: "0 -5 10 10",
		refX: 21,
		refY: 0,
		markerWidth: 5,
		markerHeight: 5,
		orient: "auto" }).append("path").attr("d", "M0,-5L10,0L0,5");

	var x = d3.scale.linear().range([0, width]); // minus a 10 pixel buffer?  we should really get the width of #chart !!!

	var links = svg.selectAll(".link"),
	    nodes = svg.selectAll(".node");

	function tick() {
		nodes.attr({
			cx: function (d) {
				return d.x;
			},
			cy: function (d) {
				return d.y;
			} });

		links.attr({
			x1: function (d) {
				return d.source.x;
			}, // d.source is an index, but somehow it knows to find the node of that index.
			y1: function (d) {
				return d.source.y;
			},
			x2: function (d) {
				return d.target.x;
			},
			y2: function (d) {
				return d.target.y;
			} });
	}

	// now that we get the data, do all the things that we can only do once the data comes:
	// pretend this works
	// d3.tsv("../data/mybargraph.tsv", d => +d.value, function(error, data){
	// pretend data comes in as a json unwrapped into a js object
	var graph = {
		nodes: [{ x: 40, y: 40 }, // 0
		{ x: 80, y: 80 }, // 1
		{ x: 160, y: 160 }, // 2
		{ x: 0, y: 20 }, // 3
		{ x: 80, y: 300 }],
		links: [{ source: 0, target: 1, fixed: true }, { source: 2, target: 3 }, { source: 3, target: 4 }] };

	x.domain([0, d3.max(_.pluck(graph.nodes, "x"))]);

	force.nodes(graph.nodes).links(graph.links).start();

	links = links.data(graph.links) // links before nodes so that lines in SVG appear *under* nodes
	.enter().append("line").classed("link", true).attr("marker-end", "url(#arrow-head)"); // add in the marker-end defined above

	nodes = nodes.data(graph.nodes).enter().append("circle").classed("node", true).attr({
		r: 12,
		fill: randColor })
	// .classed('fixed', true)
	// .on('dblclick', dblclick)
	// .on('beginEvent', node => alert('beginEvent') )
	// .on('animationend', node => alert('animationend') )
	// .on('DOMContentLoaded', node => alert('DOMContentLoaded') )
	// .on('drag', node => alert('drag') )
	// .on('endEvent', node => alert('endEvent') )
	// .on('readystatechange', node => alert('readystatechange') )
	.call(drag)
	// .call( x => alert('running') )
	// .call( node => d3.select(this).classed('fixed', node.fixed = true) )

	// })

	;
}); // end require
// 4
// these can be attributes or styles in SVG.  Both ways work.

