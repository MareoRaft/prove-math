// require and requirejs are two names for the same function.  when require gets {} input, it basically calls require.config for you
require.config({
	baseUrl: "scripts/lib", // the default base is the directory of the INDEX.HTML file
	paths: { // other paths we want to access
		jquery: "http://code.jquery.com/jquery-1.11.2.min", // and the .js is added like always by require
		// underscore: "https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.2/underscore-min",
		// backbone: "https://cdnjs.cloudflare.com/ajax/libs/backbone.js/1.1.2/backbone-min",
		d3: "https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min",
	},
	shim: { // allows us to bind variables to global (with exports) and show dependencies without using define()
		// underscore: { exports: "_" },
		// backbone: { deps: ["jquery", "underscore"], exports: "Backbone" },
	},
});

require( ["jquery", "d3", "browser-detect"], function($, d3, browser){

$('section').click( function(){ alert('jquery') } ); // jquery is smart to team up with require and include .ready() builtin, so we no longer need that wrapper around everything

var data = [4, 5, 6, 1, 8, 10]

d3.select('body').append('div').html('i am content')


// d3.select('.chart').data(data).enter().append('div')
// 	.style('width', d => d*10+'px')
// 	.text(d => d)

var x = d3.scale.linear()
	.domain([0, d3.max(data)])
	.range([0, $('#chart').width()]) // minus a 10 pixel buffer?  we should really get the width of #chart !!!


// this pattern is good because it allows UPDATING data too
d3.select("#chart").selectAll("div").data(data) // bind the data to the DIVs
	// this is where we enter new data.  there is also an update() and exit() for updating data and exiting data
	.enter().append("div")
		.style('width', d => x(d)+'px')
		.text(d => d)




// $("input[type=submit]").click( function(){
// 	var x = $("#x").val();
// 	var y = $("#y").val();
// 	$("output").val( gcd(x,y) );
// });


}); // end require
