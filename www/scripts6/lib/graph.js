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

function nodeIdsList() {
	return Object.keys(graph.nodes)
}

function nodeNamesList() {
	let node_names = []
	_.each(graph.nodes, function(node){
		node_names.push(node.name)
	})
	return node_names
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
	_.each(links, function(link){
		if (link.source === undefined) die('graph link no source. link: '+JSON.stringify(link))
	})

	graphAnimation.addNodesAndLinks({
		nodes: nodes,
		links: links,
	})
}

function _addNodesHereAndJSNetworkX(nodes) {
	_.each(nodes, function(node) {
		if( node.remove ){
			console.log('REMOVING node')
			_removeNodes([node])
		}
		else{

			if( node.id in graph.nodes ){
				console.log('redundant node')
				//die('THAT node is already in the node hash (add support for this later if it makes sense to allow this sort of thing).')
			}
			else{
				graph.nodes[node.id] = node
			}
		}
	})
	// add ids to JSnetworkx too
}

function removeNodes(nodes) {
	_.each(nodes, function(node) {
		if( !(node.id in graph.nodes) ) die("You are trying to remove a node that isn't in the graph.nodes hash.")
	})
	graphAnimation.removeNodes(nodes)
	// remove nodes (using node.id) from JSNetworkX (and any incident links will automatically go away)
	_.each(nodes, function(node){ delete graph.nodes[node.id] })
}

function removeNode(node) {
	removeNodes([node])
}

function _addLinksHereAndJSNetworkX(links) {
	// add links to JSNetworkX

	// maybe no need to have local copy of links see they don't carry any extra info.
	//update source and targets of links to point to objects, not IDs // i don't think we need this anymore!  or perhaps graph-animation likes it...
	_.each(links, function(link){
		let source_key = link.source
		let target_key = link.target

		let source_before = source_key
		link.source = graph.nodes[source_key]
		console.log('target key: '+target_key)
		console.log('taget NODE: '+JSON.stringify(graph.nodes[target_key]))
		link.target = graph.nodes[target_key]
		if( !def(link.source) ){
			$.event.trigger({
				type: 'request-node',
				message: source_before,
			})
		}
		if(!def(link.target)) die('bad target key is: '+target_key)
	})
	is.assert.array.of.object(links)
}

function removeLinks({ node_id, dependency_ids }) {
	let node = graph.nodes[node_id]

	let links = []
	_.each(dependency_ids, function(dependency_id) {
		let dependency = graph.nodes[dependency_id]

		links.push({ source: dependency, target: node })
	})
	graphAnimation.removeLinks(links)
}

function _changeNodeId(old_id, new_id) {
	if ( ! _.contains(this.nodeIdsList(), old_id) ) die('That node isn\'t in the graph to begin with.')
	if ( _.contains(this.nodeIdsList(), new_id) ) die('That id is already being used for another node!')
	this.nodes[new_id] = this.nodes[old_id]
	delete this.nodes[old_id]
	// but the problem is that the old id is still being used elsewhere in the program.  We could force the user to give the node a name so that we update the ID BEFORE setting any dependencies.
}

return {
	init: init,
	addNode: addNode,
	addNodesAndLinks: addNodesAndLinks,
	removeNode: removeNode,
	removeNodes: removeNodes,
	removeLinks: removeLinks,
	nodes: graph.nodes,
	nodeIdsList: nodeIdsList,
	nodeNamesList: nodeNamesList,
	_changeNodeId: _changeNodeId,
}

}) // end define
