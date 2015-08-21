define( ['jquery', 'underscore', 'd3', 'check-types', 'profile'], function($, _, d3, check, undefined) {


/////////////////////////////////// HELPERS ///////////////////////////////////
var nodes = [],
	links = []

function removeNodeById(id){ // assumes only one node of each id exists
	check.assert.string(id)
	for( let i in nodes )if( nodes[i]._id === id ){
		nodes.splice(i, 1)
		return true
	}
	die('No node of that id to remove.')
}

function removeLinksFromArrayById(link_array, id){
	check.assert.array.of.object(link_array)
	check.assert.string(id)
	for( let i = 0; i < link_array.length; i++ )if( link_array[i].source._id === id || link_array[i].target._id === id ){
		link_array.splice(i, 1)
		i--
	}
	return link_array
}

function removeLinksById(id){
	links = removeLinksFromArrayById(links, id)
}

function findObjectById(array, id){
	check.assert.array(array)
	check.assert.string(id)
	for( let i in array )if( array[i]._id === id ) return array[i]
	die('id not found.')
}

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

function dragstart(node) {
	d3.select(this).classed('fixed', node.fixed = true)
}

function dblclick(node) {
	d3.select(this).classed('fixed', node.fixed = false)
}


//////////////////////////////////// MAIN /////////////////////////////////////
var width = $('body').width(),
	height = $(window).height()

var force = d3.layout.force()
	.nodes(nodes) // and when we push new nodes to nodes, things happen (i think)
	.links(links)
	.size([width, height])
	.charge(-400) // all of these can be FUNCTIONS, which act on each node or link, depending on the property :)
	// .linkDistance(120) // this is too "fixed". better to use other variables to make the spacing self-create
	.linkStrength(0.2)
	.gravity(0.05)
	.on('tick', updateSVGNodeAndLinkPositions)

var drag = force.drag()
	.on('dragstart', dragstart);

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

function updateNodesAndLinks(new_graph) {
	//if a node is marked 'remove', remove it from nodes, new_graph.nodes, and links
	for( let i = 0; i < new_graph.nodes.length; i++ ){
		if( new_graph.nodes[i].empty ){
			// maybe replace it with a minimal dict and some message "please complete me!"
			console.log('Found an empty node. Letting it proceed.')
		}
		else if( new_graph.nodes[i].remove ){
			removeNodeById(new_graph.nodes[i]._id)
			removeLinksById(new_graph.nodes[i]._id) // we assume there are no links to a removed node in new_graph.links.  That is, we assume a good input.
			new_graph.nodes.splice(i, 1)
			i--
		}
		// if( id already exists )... // d3 won't duplicate an element, so we're ok here.  But a good input should probably not send over the same element again anyway...
	}
	nodes.pushArray(new_graph.nodes)
	check.assert.array.of.object(nodes)

	//update source and targets of links to point to objects, not IDs
	_.each(new_graph.links, function(link){
		link.source = findObjectById(nodes, link.source)
		link.target = findObjectById(nodes, link.target)
	})
	links.pushArray(new_graph.links)
	check.assert.array.of.object(links)
}

function updateSVGNodeAndLinkExistence() { // this function gets called AGAIN when new nodes come in
    var link = svg.selectAll('.link').data(force.links(), d => d.source._id + '--->' + d.target._id) // links before nodes so that lines in SVG appear *under* nodes
    link.enter().append('line')
    	.classed('link', true)
    	.attr('marker-end', 'url(#arrow-head)') // add in the marker-end defined above
    link.exit().remove()

	var node = svg.selectAll('.node').data(force.nodes(), d => d._id)
		var node_group = node.enter().append('g')
			.classed('node', true)
			.call(drag)
			.on('dblclick', dblclick)
		node_group.append('circle')
		    .classed('node-circle', true)
			.classed('definition-circle', d => d._type === 'definition')
			.classed('theorem-circle', d => d._type === 'theorem')
			.classed('exercise-circle', d => d._type === 'exercise')
	    	.attr({ // we may consider adding the position too. it will get updated on the next tick anyway, so we will only add it here if things look glitchy
	    		r: d => 6 * Math.sqrt(d._importance),
	    	})
	    node_group.append('text') // must appear ABOVE node-circle
		    .classed('node-text', true)
			.text(function(d){ if(d._type !== 'exercise') return d._name }) // exercise names should NOT appear
    node.exit().remove()


}

function processNewGraph(new_graph) {
	updateNodesAndLinks(new_graph);
	// x.domain([0, d3.max(_.pluck(nodes, 'x'))]) // not sure where in the flow this belongs...
	updateSVGNodeAndLinkExistence(); // nodes and links variables are global
	force.start()
}

return {
	processNewGraph: processNewGraph,
}


}); // end of define
