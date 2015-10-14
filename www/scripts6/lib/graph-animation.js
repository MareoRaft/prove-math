define(["jquery", "check-types", "profile", "d3", "user"], function($, check, undefined, d3, user){

let gA = {} // for graphAnimation
function init(input) {
	gA = _.defaults(input, {
		// window_id, // due to select() issue having to use 'body'
		nodes: [],
		links: [],
		node_id: function(node){ if( !def(node) ) die('got undefined node.'); return node.id },
		node_label: '',
		node_radius: node => node.r,
		circle_class_conditions: {},
		circle_events: {},
	})

	gA.circle_events = _.mapObject(gA.circle_events, function(func) {
		return function(node) { func(node); update() }
	})

	// if( !def(window_id) ) die('No window_id (id of html container) given to initialize graphAnimation in.')
	// gA.$window = $('#' + window_id)
	// gA.width = gA.$window.width(),
	// gA.height = gA.$window.height()
	gA.width = $(window).width()
	gA.height = $(window).height()

	gA.force = d3.layout.force() // see https://github.com/mbostock/d3/wiki/Force-Layout for options
		.nodes(gA.nodes) // and when we push new nodes to nodes, things happen (i think)
		.links(gA.links)
		.size([gA.width, gA.height])
		.charge(-400) // all of these can be FUNCTIONS, which act on each node or link, depending on the property :)
		// .linkDistance(120) // this is too "fixed". better to use other variables to make the spacing self-create
		.linkStrength(0.2)
		.gravity(0.05)
		.alpha(0.2)
		// .theta(1.5) // this enables approximation for charge interaction, which may be needed for large graphs or slow browsers.  Higher numbers are more approximation.  I wouldn't go any higher than 1.5 though.
		.on('tick', _tick)

	//we can't override force.tick easily. but we want the line change:
		// if ((alpha *= .99) < .005) {
	    // to
		// if ((alpha *= .995) < .0045) {
	gA.force.resume = function() {
		let alpha = gA.force.alpha()
		if( alpha < 0.0045 ){ alpha = 0.0050 } // assuming a cutoff of 0.0045.  That means for now, we are dependent on serving a customized version of d3 to users, even though its only one line change.  We could change it to 0.0050 and 0.0055 if we had to.
		else if( alpha < 0.11 ){ alpha += 0.0006 }
		return gA.force.alpha(alpha)
	}

	gA.drag = gA.force.drag()

	gA.svg = d3.select('body') // select() only seems to work on 'body', but not on any '#id's!!!! :(
		.append('svg')
			.attr({
				width: gA.width,
				height: gA.height,
			})

	gA.svg.append('defs').attr('fill', 'green').selectAll('marker').data(['arrow-head']) // binding 'arrow-head' is our way of attaching a name!
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

	gA.x = d3.scale.linear()
		.range([0, gA.width])

	if( gA.nodes.length > 0 ) _start()
}

function _start() {
	gA.force.start() // well, we actually only want this when there has been a change in node or link presence.  A mere change of name is not enough.  If we could autodetect such changes, then this could be integrated into update() instead of making user trigger it manually
}

function _tick(){
	gA.svg.selectAll('.node')
		.attr({
			transform: node => 'translate('+node.x+','+node.y+')',
		})
	gA.svg.selectAll('.link')
		.attr({
			x1: node => node.source.x,
			y1: node => node.source.y,
			x2: node => node.target.x,
			y2: node => node.target.y,
		})
}

function update() { // this function gets called AGAIN when new nodes come in
	// x.domain([0, d3.max(_.pluck(nodes, 'x'))]) // not sure where in the flow this belongs...

// it was a LINK ISSUE!  you need to go over entire link importation stuff to verify it makes sense
    let link = gA.svg.selectAll('.link').data(gA.force.links(), link => gA.node_id(link.source) + '--->' + gA.node_id(link.target)) // links before nodes so that lines in SVG appear *under* nodes
    link.enter().append('line')
    	.classed('link', true)
    	.attr('marker-end', 'url(#arrow-head)') // add in the marker-end defined above
    link.exit().remove()

	let node = gA.svg.selectAll('.node').data(gA.force.nodes(), gA.node_id)
		let node_group = node.enter().append('g')
			.classed('node', true)
			.call(gA.drag)
		node_group.append('circle')
		    .classed('node-circle', true)
			.attr('r', gA.node_radius) // we may consider adding the position too. it will get updated on the next tick anyway, so we will only add it here if things look glitchy
			.on(gA.circle_events)
		node_group.append('text') // must appear ABOVE node-circle
		    .classed('node-text', true)
    node.exit().remove()

    // UPDATE stuff (things we need to update even if we are not enter()ing the node for the first time
    gA.svg.selectAll('.node-text')
		.text(gA.node_label)
	gA.svg.selectAll('circle')
		.classed(gA.circle_class_conditions)
}

function addNodesAndLinks({ nodes=[], links=[] }) {
	// $.extend(gA.nodes, nodes) // but this is no good for duplicates. switch to hash soon
	_.each(nodes, function(node){ if (node === undefined) die('before. undefined node in gA.addNodesAndLinks') })
	gA.nodes.pushArray(nodes)
	// $.extend(gA.links, links)
	gA.links.pushArray(links)
	// maybe get smart here and detect whether there actually was a change or not.  can d3 do this?
	_.each(gA.nodes, function(node){ if (node === undefined) die('after. undefined node in gA.addNodesAndLinks') })
	update()
	_.each(gA.nodes, function(node){ if (node === undefined) die('bwt update n start. undefined node in gA.addNodesAndLinks') })
	_start()
	_.each(gA.nodes, function(node){ if (node === undefined) die('END. undefined node in gA.addNodesAndLinks') })
}

function removeNodes(nodes) {
	_.each(nodes, function(node) {
		_.each(gA.nodes, function(gA_node, index) {
			if( node.id === gA_node.id ) gA.nodes.remove(index)
		})
	})
	update()
	_start()
}

return {
	init: init,
	addNodesAndLinks: addNodesAndLinks,
	removeNodes: removeNodes,
	update: update,
}

}) // end define
