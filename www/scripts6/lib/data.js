define( [
	'jquery','underscore', 'check-types', 'profile', 'd3-and-svg', 'user', 'marked'],
	function(
	$,        _,            check,         undefined, d3AndSVG,     user,   marked) {


/////////////////////////////////// HELPERS ///////////////////////////////////
function removeParenthesizedThing(string){
	return string.replace(/\([^\)]*\)/, '');
}

function removeOneContextFromNames(){
	// go through nodes and update the displayNames to be the _names with removal (above function)
	_.each(d3AndSVG.nodes, function(node){
		node.displayName = removeParenthesizedThing( node.name )
	})
	// after the loop is completed, kickoff the d3 restart, which should trigger the UPDATE automatically
	d3AndSVG.processNewGraph() // nodes and links variables are global
}

function showFullContextInNames(){
	_.each(d3AndSVG.nodes, function(node){
		node.displayName = node.name
	})
	d3AndSVG.processNewGraph()
}

function updateDisplayNameCapitalization(){
	_.each(d3AndSVG.nodes, function(node){
		switch (user.prefs.displayNameCapitalization){
			case null:
				node.displayName = node.name
				break
			case "sentence":
				node.displayName = node.name.capitalizeFirstLetter()
				break
			case "title":
				// for each word in node.name, capitalize it unless it's in the small words list
				var smallWordsList = [
					//nice guide // see http://www.superheronation.com/2011/08/16/words-that-should-not-be-capitalized-in-titles/
					//================
					// articles
					// --------------
					'a', 'an', 'the',
					// coordinate conjunctions
					// ---------------------------
					'for', 'and', 'nor', 'but', 'or', 'yet', 'so',
					// prepositions // there are actually A LOT of prepositions, but we'll just tackle the most common ones. for a full list, see https://en.wikipedia.org/wiki/List_of_English_prepositions
					// --------------------
					'at', 'around', 'by', 'after', 'along', 'for', 'from', 'in', 'into', 'minus', 'of', 'on', 'per', 'plus', 'qua', 'sans', 'since', 'to', 'than', 'times', 'up', 'via', 'with', 'without',
				]
				node.displayName = node.name.replace(/\b\w+\b/g, function(match){
					if( !_.contains(smallWordsList, match) ){
						match = match.capitalizeFirstLetter()
					}
					return match
				})
				// first and last word must be capitalized always!!!
				node.displayName = node.displayName.capitalizeFirstLetter()
				node.displayName = node.displayName.replace(/\b\w+\b$/g, match => match.capitalizeFirstLetter())
				break
			default:
				die('Unrecognized displayNameCapitalization preference value "'+user.prefs.displayNameCapitalization+'".')
		}
	})
}

function updateDisplayName(node) { // for a single node
	node.displayName = node.name
	// node.displayName = updateDisplayNameContext
	// updateDisplayNameCapitalization() // but for a single node
}


//////////////////////////////// NODE OBJECTS /////////////////////////////////
function removeNodeById(id){ // assumes only one node of each id exists
	check.assert.string(id)
	for( let i in d3AndSVG.nodes )if( d3AndSVG.nodes[i].id === id ){
		d3AndSVG.nodes.splice(i, 1)
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
	d3AndSVG.links = removeLinksFromArrayById(d3AndSVG.links, id)
}

function findObjectById(array, id){
	check.assert.array(array)
	check.assert.string(id)
	for( let i in array )if( array[i].id === id ) return array[i]
	die('id not found.')
}

function removeLeadingUnderscoresFromKeys(obj) {
	_.each(obj, function(value, key){ if( key[0] === '_' ){
		delete obj[key]
		key = key.substr(1)
		obj[key] = value
	}})
	return obj
}

function addNewNodes(new_nodes) {
	_.each(new_nodes, function(new_node){
		new_node = removeLeadingUnderscoresFromKeys(new_node)
		new_node.displayName = new_node.name
	})
	d3AndSVG.nodes.pushArray(new_nodes)
	check.assert.array.of.object(d3AndSVG.nodes)
}

function updateNodesAndLinks(new_graph) {
	//if a node is marked 'remove', remove it from nodes, new_graph.nodes, and links
	for( let i = 0; i < new_graph.nodes.length; i++ ){
		if( new_graph.nodes[i].empty ){
			// maybe replace it with a minimal dict and some message "please complete me!"
			console.log('Found an empty node. Letting it proceed.')
		}
		else if( new_graph.nodes[i].remove ){
			removeNodeById(new_graph.nodes[i].id)
			removeLinksById(new_graph.nodes[i].id) // we assume there are no links to a removed node in new_graph.links.  That is, we assume a good input.
			new_graph.nodes.splice(i, 1)
			i--
		}
		// if( id already exists )... // d3 won't duplicate an element, so we're ok here.  But a good input should probably not send over the same element again anyway...
	}

	addNewNodes(new_graph.nodes)

	//update source and targets of links to point to objects, not IDs
	_.each(new_graph.links, function(link){
		link.source = findObjectById(d3AndSVG.nodes, link.source)
		link.target = findObjectById(d3AndSVG.nodes, link.target)
	})
	d3AndSVG.links.pushArray(new_graph.links)
	check.assert.array.of.object(d3AndSVG.links)

	d3AndSVG.processNewGraph(new_graph)
}

//////////////////////////////////// MAIN /////////////////////////////////////
return {
	updateNodesAndLinks: updateNodesAndLinks,
	removeOneContextFromNames: removeOneContextFromNames,
	showFullContextInNames: showFullContextInNames,
	updateDisplayNameCapitalization: updateDisplayNameCapitalization,
	updateDisplayName: updateDisplayName,
}


}); // end of define
