define(['jquery', 'underscore', 'check-types', 'profile'], function($, _, check, undefined) {


/////////////////////////////////// HELPERS ///////////////////////////////////
//////////////////////////////////// MAIN /////////////////////////////////////

let user = {
	prefs: {
		display_name_capitalization: "title", // can be null, "sentence", or "title"
		underline_definitions: false, // can be true or false // do you want definitions to be underlined in the DAG view?
		show_description_on_hover: false, // can be true or false
	},
	learned_node_ids: [],
}
function init({
			account_type = 'local', // can be 'local', 'facebook', 'google', 'twitter', etc...
			username,
			password, // for security reasons, don't actually store this onto user.
		}) {
	user.account_type = account_type
	user.username = username

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
	_save()
}

function unlearnNode(node) {
	if( !hasLearned(node) ) die('Tried to unlearn a node that was *not* learned (maybe you just clicked "unlearn" twice).')
	user.learned_node_ids = _.without(user.learned_node_ids, node.id)
	_save()
}

function hasLearned(node) {
	return _.contains(user.learned_node_ids, node.id)
}

function nodesAndPrefs() {}

function _save() { // to actually save back to server

}

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
