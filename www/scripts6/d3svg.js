// require and requirejs are two names for the same function.  when require gets {} input, it basically calls require.config for you
require.config({
	baseUrl: "scripts/lib", // the default base is the directory of the INDEX.HTML file
	paths: { // other paths we want to access
		jquery: "http://code.jquery.com/jquery-1.11.2.min", // and the .js is added like always by require
		underscore: "https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.2/underscore-min",
		// backbone: "https://cdnjs.cloudflare.com/ajax/libs/backbone.js/1.1.2/backbone-min",
		d3: "https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min",
	},
	shim: { // allows us to bind variables to global (with exports) and show dependencies without using define()
		// underscore: { exports: "_" },
		// backbone: { deps: ["jquery", "underscore"], exports: "Backbone" },
	},
});

require( ["jquery", "underscore", "d3", "browser-detect"], function($, _, d3, browser){

$('section').click( function(){ alert('jquery') } ); // jquery is smart to team up with require and include .ready() builtin, so we no longer need that wrapper around everything


var barHeight = 15

var x = d3.scale.linear()
	.range([0, $('#chart').width()]) // minus a 10 pixel buffer?  we should really get the width of #chart !!!

// pretend this works
// d3.tsv("../data/mybargraph.tsv", d => +d.value, function(error, data){
	// pretend data comes in as a json unwrapped into a js object
	var data = [
	  {name: "Locke",    value:  4},
	  {name: "Reyes",    value:  8},
	  {name: "Ford",     value: 15},
	  {name: "Jarrah",   value: 16},
	  {name: "Shephard", value: 23},
	  {name: "Kwon",     value: 42},
	]
	data = _.pluck(data, 'value') // change data to an array

	x.domain([0, d3.max(data)])

	var chart = d3.select('#chart')
		.attr('height', data.length * barHeight)

	// this pattern is good because it allows UPDATING data too
	var bar = chart.selectAll('g').data(data) // bind the data to the DIVs
		// this is where we enter new data.  there is also an update() and exit() for updating data and exiting data
		.enter().append('g')
			.attr('transform', (d,i) => 'translate(0,' + i * barHeight + ')')

	bar.append('rect')
		.attr('width', d => x(d))
		.attr('height', barHeight)

	bar.append('text')
		.attr('x', d => x(d) - 3)
		.attr('y', barHeight / 2)
		.attr('dy', '.35em')
		.text(d => d)
// })







}); // end require
