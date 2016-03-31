define(['jquery', 'underscore', 'profile', 'check-types'], function($, _, undefined, is) {


/////////////////////////////////// HELPERS ///////////////////////////////////
//////////////////////////////////// MAIN /////////////////////////////////////
let user = {
	account: {
		type: "local",
		id: null,
	},
	prefs: {
		display_name_capitalization: null, // can be null, "sentence", or "title"
		underline_definitions: false, // can be true or false // do you want definitions to be underlined in the DAG view?
		show_description_on_hover: false, // can be true or false
		// view_node_trigger: 'dblclick', // can be dblclick or click // obsolete
		animate_blinds: false,
	},
	learned_node_ids: [],
}
function init(dict) { // this must handle empty input before user logs in, and the real user account init when they log in
	$.extend(true, user, dict) // the first parameter means DEEP extend
}

function _login(password) {
	die('Login not yet implemented.')
	// bla bla oauth.
	// user.account_type, user.username, password
	// return oauth object
}

// function learnedNodeIds() {} // getter

function learnNode(node) {
	if( hasLearned(node) ) die('Tried to learn a node that was already learned (maybe you just clicked "learn" twice).')
	user.learned_node_ids.push(node.id)
	$.event.trigger({
		type: 'jsend',
		message: { command: 'learn-node', node_id: node.id, mode: 'learn' },
	})
}

function unlearnNode(node) {
	if( !hasLearned(node) ) die('Tried to unlearn a node that was *not* learned (maybe you just clicked "unlearn" twice).')
	user.learned_node_ids = _.without(user.learned_node_ids, node.id)
	$.event.trigger({
		type: 'jsend',
		message: { command: 'unlearn-node', node_id: node.id },
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
		type: 'jsend',
		message: { command: 'set-pref', pref_dict: dic },
	})
}

function nodesAndPrefs() {}

function identifier(){
	return {
		type: user.account.type,
		id: user.account.id,
	}
}

function update_identifier(identifier){
	if( identifier ){
		if( identifier['type'] !== 'local' ){
			// pass, since the user must be logged in
		}
		else if( is.not.null(user.account.id) && user.account.id !== identifier['id'] ){
			die('New id is different than defined old id!')
		}
		else{
			user.account.id = identifier['id']
		}
	}
}

return {
	init: init,
	accountType: user.account_type,
	username: user.username,
	prefs: user.prefs,
	learnNode: learnNode,
	unlearnNode: unlearnNode,
	hasLearned: hasLearned,
	setPref: setPref,
	get_identifier: identifier,
	update_identifier: update_identifier,
}

}) // end of define
