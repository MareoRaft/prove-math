define(["underscore", "check-types", "graph-animation", /*"jsnetworkx"*/],
function(_,            is,            graphAnimation/*, jsNetworkX*/) {

let graph = {
	nodes: {},
	links: [],
}
function init(nodes=[], links=[]) {
	die('maybe not finished writing this init function yet')
	// create blank jsNetworkX graph
	addNodesAndLinks({
		nodes: nodes,
		links: links,
	})
}

function addNode(node) {
	addNodesAndLinks({
		nodes: [node],
	})
}

function addNodesAndLinks({ nodes=[], links=[] }) {
	_.each(nodes, function(node){ if (node === undefined) die('before. undefined node in graph.addNodesAndLinks') })
	_addNodesHereAndJSNetworkX(nodes)
	_addLinksHereAndJSNetworkX(links)
	// see from JSNetworkX which things we should add to the animation:
	_.each(nodes, function(node){ if (node === undefined) die('after. undefined node in graph.addNodesAndLinks') })
	graphAnimation.addNodesAndLinks({
		nodes: nodes,
		links: links,
	})
}

function _addNodesHereAndJSNetworkX(nodes) {
	let temparr = []
	_.each(nodes, function(node) {
		temparr.push(node.id)
	})
	// alert(temparr)

	_.each(nodes, function(node) {
		if( node.remove ){
			_removeNodes([node])
		}
		else{
			if( node.id in graph.nodes ){
				//die('THAT node is already in the node hash (add support for this later if it makes sense to allow this sort of thing).')
			}
			else{
				graph.nodes[node.id] = node
			}
		}
	})
	// add ids to JSnetworkx too
}

function _removeNodes(nodes) {
	_.each(nodes, function(node) {
		if( !(node.id in graph.nodes) ) die("You are trying to remove a node that isn't in the graph.nodes hash.")
	})
	graphAnimation.removeNodes(nodes)
	// remove nodes (using node.id) from JSNetworkX (and any incident links will automatically go away)
	_.each(nodes, function(node){ delete graph.nodes[node.id] })
}

// function findObjectById(array, id){ // delete THIS WHEN SWITCHING TO HASH
// 	is.assert.array(array)
// 	is.assert.string(id)
// 	for( let i in array )if( array[i].id === id ) return array[i]
// 	die('id not found.')
// }

function _addLinksHereAndJSNetworkX(links) {
	// add links to JSNetworkX

	// maybe no need to have local copy of links see they don't carry any extra info.
	//update source and targets of links to point to objects, not IDs // i don't think we need this anymore!  or perhaps graph-animation likes it...
	_.each(links, function(link){
		let source_key = link.source
		let target_key = link.target

		let source_before = link.source
		link.source = graph.nodes[link.source]
		link.target = graph.nodes[link.target]
		if( !def(link.source) ){
			alert('bad source key is: '+source_key+'.  Sending request!')
			$.event.trigger({
				type: 'request-node',
				message: source_before,
			})
		}
		if(!def(link.target)) die('bad target key is: '+target_key)
		// link.source = findObjectById(graph.nodes, link.source)
		// link.target = findObjectById(graph.nodes, link.target)
	})
	is.assert.array.of.object(links)
}

function _removeLinks() {
	die('Link removing not yet added.')
}

return {
	init: init,
	addNode: addNode,
	addNodesAndLinks: addNodesAndLinks,
	nodes: graph.nodes,
}

}) // end define
