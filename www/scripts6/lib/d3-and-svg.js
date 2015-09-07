define( ['jquery', 'underscore', 'd3', 'check-types', 'profile', 'user'], function($, _, d3, check, undefined, user) {


/////////////////////////////////// HELPERS ///////////////////////////////////
function updateSVGNodeAndLinkPositions(){
	svg.selectAll('.node')
		.attr({
			transform: d => 'translate('+d.x+','+d.y+')',
		})
	svg.selectAll('.link')
		.attr({
			x1: d => d.source.x,
			y1: d => d.source.y,
			x2: d => d.target.x,
			y2: d => d.target.y,
		})
}

function mouseover(node) {
	if( user.prefs.showDescriptionOnHover ){
		node.displayName = node._description
		updateSVGNodeAndLinkExistence()
	}
}

function mouseout(node) {
	if( user.prefs.showDescriptionOnHover ){
		node.displayName = node._name
		updateSVGNodeAndLinkExistence()
	}
}

function dblclick(node) {
	// d3.select(this).classed('fixed', node.fixed = false)
}

// function dragstart(node) {
// 	// d3.select(this).classed('fixed', node.fixed = true)
// }

// function dragstart(node) {
// 	d3.event.sourceEvent.stopPropagation();
// 	force.start();
// }

// function drag(node) {
// 	d3.select(this).attr("cx", node.x = d3.event.x).attr("cy", node.y = d3.event.y);
// }

//////////////////////////////////// MAIN /////////////////////////////////////
var nodes = [],
	links = []

var width = $(window).width(),
	height = $(window).height()

var force = d3.layout.force() // see https://github.com/mbostock/d3/wiki/Force-Layout for options
	.nodes(nodes) // and when we push new nodes to nodes, things happen (i think)
	.links(links)
	.size([width, height])
	.charge(-400) // all of these can be FUNCTIONS, which act on each node or link, depending on the property :)
	// .linkDistance(120) // this is too "fixed". better to use other variables to make the spacing self-create
	.linkStrength(0.2)
	.gravity(0.05)
	.alpha(0.2)
	// .theta(1.5) // this enables approximation for charge interaction, which may be needed for large graphs or slow browsers.  Higher numbers are more approximation.  I wouldn't go any higher than 1.5 though.
	.on('tick', updateSVGNodeAndLinkPositions)

//we can't override force.tick easily. but we want the line change:
	// if ((alpha *= .99) < .005) {
    // to
	// if ((alpha *= .995) < .0045) {
force.resume = function() {
  var alpha = force.alpha()
  if( alpha < 0.0045 ){ alpha = 0.0050 } // assuming a cutoff of 0.0045.  That means for now, we are dependent on serving a customized version of d3 to users, even though its only one line change.  We could change it to 0.0050 and 0.0055 if we had to.
  else if( alpha < 0.11 ){ alpha += 0.0006 }
  return force.alpha(alpha);
};

var drag = force.drag()
	// .on('dragstart', dragstart);

var svg = d3.select('body')
	.append('svg')
		.attr({
			width: width,
			height: height,
		})

svg.append('defs').attr('fill', 'green').selectAll('marker').data(['arrow-head']) // binding 'arrow-head' is our way of attaching a name!
	.enter().append('marker')
		.classed('arrow-head', true)
    	.attr({
    		id: String,
    		viewBox: '0 -5 10 10',
	    	refX: 21,
	    	refY: 0,
	    	markerWidth: 5,
	    	markerHeight: 5,
	    	orient: 'auto',
	    })
  		.append('path')
			.attr('d', 'M0,-5L10,0L0,5')

var x = d3.scale.linear()
	.range([0, width]) // minus a 10 pixel buffer?  we should really get the width of #chart !!!

function updateSVGNodeAndLinkExistence() { // this function gets called AGAIN when new nodes come in
    var link = svg.selectAll('.link').data(force.links(), d => d.source._id + '--->' + d.target._id) // links before nodes so that lines in SVG appear *under* nodes
    link.enter().append('line')
    	.classed('link', true)
    	.attr('marker-end', 'url(#arrow-head)') // add in the marker-end defined above
    link.exit().remove()

	var node = svg.selectAll('.node').data(force.nodes(), d => d._id)
		var node_group = node.enter().append('g')
			.classed('node', true)
			// .id(d => d._id)
			.call(drag)
		node_group.append('circle')
		    .classed('node-circle', true)
			.classed('definition-circle', d => d._type === 'definition')
			.classed('theorem-circle', d => d._type === 'theorem')
			.classed('exercise-circle', d => d._type === 'exercise')
			.attr({ // we may consider adding the position too. it will get updated on the next tick anyway, so we will only add it here if things look glitchy
				r: d => 6 * Math.sqrt(d._importance),
			})
			.on('dblclick', dblclick)
			.on('mouseover', mouseover)
			.on('mouseout', mouseout)
		node_group.append('text') // must appear ABOVE node-circle
		    .classed('node-text', true)
			.text(function(d){ if(d._type !== 'exercise') return d.displayName }) // exercise names should NOT appear
    node.exit().remove()

    // UPDATE stuff:  // more to add later!
    svg.selectAll('.node-text')
		.text(function(d){ if(d._type !== 'exercise') return d.displayName })
}

function processNewGraph() {
	// x.domain([0, d3.max(_.pluck(nodes, 'x'))]) // not sure where in the flow this belongs...
	updateSVGNodeAndLinkExistence(); // nodes and links variables are global
	force.start()
}


return {
	nodes: nodes,
	links: links,
	processNewGraph: processNewGraph,
	updateSVGNodeAndLinkExistence: updateSVGNodeAndLinkExistence,
}


}); // end of define
