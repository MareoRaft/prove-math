define(['jquery', 'underscore', 'check-types', 'profile'], function($, _, check, undefined) {


/////////////////////////////////// HELPERS ///////////////////////////////////
//////////////////////////////////// MAIN /////////////////////////////////////
let user = {
	prefs: {
		display_name_capitalization: "title", // can be null, "sentence", or "title"
		underline_definitions: false, // can be true or false // do you want definitions to be underlined in the DAG view?
		show_description_on_hover: false, // can be true or false
		view_node_trigger: 'dblclick', // can be dblclick or click
		animate_blinds: true,
	},
	learned_node_ids: [],
}
function init(dict) { // this must handle empty input before user logs in, and the real user account init when they log in
	_.defaults(dict, {
		account_type: 'local', // can be 'local', 'facebook', 'google', 'twitter', etc...
		username: undefined,
		password: undefined, // for security reasons, don't actually store this onto user.
	})
	_.extend(user, dict)

	// user.oauth = _login(password)
	_.extend(user.prefs, _loadPrefs())
	// user.learned_node_ids
	// alert(JSON.stringify(user.prefs))
}

function _login(password) {
	die('Login not yet implemented.')
	// bla bla oauth.
	// user.account_type, user.username, password
	// return oauth object
}

function _loadPrefs() { // gets prefs from server
	return {show_description_on_hover: true} // just for testing purposes
	// die('oauth retrieval not implemented.')
	// return user.oauth.get( prefs request )
}

// function learnedNodeIds() {} // getter

function learnNode(node) {
	if( hasLearned(node) ) die('Tried to learn a node that was already learned (maybe you just clicked "learn" twice).')
	user.learned_node_ids.push(node.id)
	$.event.trigger({
		type: 'learned-node-to-server',
		message: node.id,
		date: new Date(),
	})
}

function unlearnNode(node) {
	if( !hasLearned(node) ) die('Tried to unlearn a node that was *not* learned (maybe you just clicked "unlearn" twice).')
	user.learned_node_ids = _.without(user.learned_node_ids, node.id)
	$.event.trigger({
		type: 'unlearned-node-to-server',
		message: node.id,
		date: new Date(),
	})
}

function hasLearned(node) {
	return _.contains(user.learned_node_ids, node.id)
}

function setPref(dic) {
	_.extend(user.prefs, dic)
	// maybe check for an error here that no preference was actually changed.
	// if there was a change...
	$.event.trigger({
		type: 'pref-to-server',
		message: dic,
		date: new Date(),
	})
}

function nodesAndPrefs() {}

return {
	init: init,
	accountType: user.account_type,
	username: user.username,
	prefs: user.prefs,
	learnNode: learnNode,
	unlearnNode: unlearnNode,
	hasLearned: hasLearned,
}

}) // end of define
