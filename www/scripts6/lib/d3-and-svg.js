define( ["jquery", "underscore", "d3", "check-types", "profile"], function($, _, d3, check, undefined) {


/////////////////////////////////// HELPERS ///////////////////////////////////
var nodes = [],
	links = []

function removeNodeById(id){ // assumes only one node of each id exists
	check.assert.string(id)
	for( let i in nodes )if( nodes[i].id === id ){
		nodes.splice(i, 1)
		return true
	}
	die('No node of that id to remove.')
}

function removeLinksFromArrayById(link_array, id){
	check.assert.array.of.object(link_array)
	check.assert.string(id)
	for( let i = 0; i < link_array.length; i++ )if( link_array[i].source.id === id || link_array[i].target.id === id ){
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
	for( let i in array )if( array[i].id === id ) return array[i]
	die('id not found.')
}

function updateSVGNodeAndLinkPositions(){
	svg.selectAll(".node")
		.attr({
			transform: d => "translate("+d.x+","+d.y+")",
		})
		// .attr({
		// 	cx: d => d.x,
		// 	cy: d => d.y,
		// })
		// .attr({
		// 	x: d => d.x,
		// 	y: d => d.y,
		// })

	// svg.selectAll(".node")
	// 	.attr({
	// 		dx: 0,
	// 		dy: 0,
	// 	})



	svg.selectAll(".link")
		.attr({
			x1: d => d.source.x, // d.source is an index, but somehow it knows to find the node of that index.
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
	.charge(-200)
	.linkDistance(40)
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
	//if a node is marked 'remove', remove it from nodes and new_graph.nodes
	for( let i = 0; i < new_graph.nodes.length; i++ ){
		if( new_graph.nodes[i].remove ){
			removeNodeById(new_graph.nodes[i].id)
			removeLinksById(new_graph.nodes[i].id)
			new_graph.nodes.splice(i, 1)
			i--
		}
		// if( id already exists ){
		// 	die
		// }
	}
	nodes.pushArray(new_graph.nodes)
	check.assert.array.of.object(nodes)

	//update source and targets of links to point to objects, not IDs (uncomment this after adding nodes works)
	_.each(new_graph.links, function(link){
		link.source = findObjectById(nodes, link.source)
		link.target = findObjectById(nodes, link.target)
	})
	links.pushArray(new_graph.links)
	check.assert.array.of.object(links)
}

function updateSVGNodeAndLinkExistence() { // this function gets called AGAIN when new nodes come in
    var link = svg.selectAll('.link').data(force.links(), d => d.source.id + '-' + d.target.id) // links before nodes so that lines in SVG appear *under* nodes
    link.enter().append('line')
    	.classed('link', true)
    	.attr('marker-end', 'url(#arrow-head)') // add in the marker-end defined above
    link.exit().remove()

	var node = svg.selectAll('.node').data(force.nodes(), d => d.id)
		var nodeGroup = node.enter().append('g')
			.classed('node', true)
			.call(drag)
			.on("dblclick", dblclick)
		nodeGroup.append('circle')
		    .classed('node-circle', true)
	    	.attr({ // we may consider adding the position too. it will get updated on the next tick anyway, so we will only add it here if things look glitchy
	    	// 	r: d => Math.sqrt(d.weight),
		    	r: 12,
	    	})
	    nodeGroup.append('text') // must appear ABOVE node
		    .classed('node-text', true)
			.text("some string")
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
