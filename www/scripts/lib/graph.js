"use strict";

define(["underscore", "check-types", "graph-animation"], function (_, is, graphAnimation /*, jsNetworkX*/) {

	var graph = {
		nodes: {},
		links: [] };
	function init() {
		var nodes = arguments[0] === undefined ? [] : arguments[0];
		var links = arguments[1] === undefined ? [] : arguments[1];

		die("maybe not finished writing this init function yet");
		// create blank jsNetworkX graph
		addNodesAndLinks({
			nodes: nodes,
			links: links });
	}

	function nodeIdsList() {
		return Object.keys(graph.nodes);
	}

	function nodeNamesList() {
		var node_names = [];
		_.each(graph.nodes, function (node) {
			node_names.push(node.name);
		});
		return node_names;
	}

	function addNode(node) {
		addNodesAndLinks({
			nodes: [node] });
	}

	function addNodesAndLinks(_ref) {
		var _ref$nodes = _ref.nodes;
		var nodes = _ref$nodes === undefined ? [] : _ref$nodes;
		var _ref$links = _ref.links;
		var links = _ref$links === undefined ? [] : _ref$links;

		_.each(nodes, function (node) {
			if (node === undefined) die("before. undefined node in graph.addNodesAndLinks");
		});
		_addNodesHereAndJSNetworkX(nodes);
		_addLinksHereAndJSNetworkX(links);
		// see from JSNetworkX which things we should add to the animation:
		_.each(nodes, function (node) {
			if (node === undefined) die("after. undefined node in graph.addNodesAndLinks");
		});
		_.each(links, function (link) {
			if (link.source === undefined) die("graph link no source. link: " + JSON.stringify(link));
		});

		graphAnimation.addNodesAndLinks({
			nodes: nodes,
			links: links });
	}

	function _addNodesHereAndJSNetworkX(nodes) {
		_.each(nodes, function (node) {
			if (node.remove) {
				_removeNodes([node]);
			} else {
				if (node.id in graph.nodes) {} else {
					graph.nodes[node.id] = node;
				}
			}
		});
	}

	function removeNodes(nodes) {
		_.each(nodes, function (node) {
			if (!(node.id in graph.nodes)) die("You are trying to remove a node that isn't in the graph.nodes hash.");
		});
		graphAnimation.removeNodes(nodes);
		// remove nodes (using node.id) from JSNetworkX (and any incident links will automatically go away)
		_.each(nodes, function (node) {
			delete graph.nodes[node.id];
		});
	}

	function removeNode(node) {
		removeNodes([node]);
	}

	function _addLinksHereAndJSNetworkX(links) {
		// add links to JSNetworkX

		// maybe no need to have local copy of links see they don't carry any extra info.
		//update source and targets of links to point to objects, not IDs // i don't think we need this anymore!  or perhaps graph-animation likes it...
		_.each(links, function (link) {
			var source_key = link.source;
			var target_key = link.target;

			var source_before = link.source;
			link.source = graph.nodes[link.source];
			link.target = graph.nodes[link.target];
			if (!def(link.source)) {
				$.event.trigger({
					type: "request-node",
					message: source_before });
			}
			if (!def(link.target)) die("bad target key is: " + target_key);
		});
		is.assert.array.of.object(links);
	}

	function removeLinks(_ref) {
		var node_id = _ref.node_id;
		var dependency_ids = _ref.dependency_ids;

		var node = graph.nodes[node_id];

		var links = [];
		_.each(dependency_ids, function (dependency_id) {
			var dependency = graph.nodes[dependency_id];

			links.push({ source: dependency, target: node });
		});
		graphAnimation.removeLinks(links);
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
		nodeNamesList: nodeNamesList };
}); /*"jsnetworkx"*/
//die('THAT node is already in the node hash (add support for this later if it makes sense to allow this sort of thing).')
// add ids to JSnetworkx too
// end define

