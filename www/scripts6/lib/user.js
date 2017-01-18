define(['jquery', 'underscore', 'profile', 'check-types'], function($, _, undefined, is) {


/////////////////////////////////// HELPERS ///////////////////////////////////
//////////////////////////////////// MAIN /////////////////////////////////////
let user = {
	account: {
		type: "local",
		id: null,
	},
	prefs: {
		new_node_default_type: 'definition', // can be 'definition', 'theorem', 'axiom', or 'exercise'
		// 'write' state DOESNT FULLY WORK YET
		open_node_default_state: 'read', // can be 'read' or 'write'
		// visuals
		display_number_instead_of_name: true, // can true or false.
		display_name_capitalization: null, // can be null, "sentence", or "title"
		underline_definitions: false, // can be true or false // do you want definitions to be underlined in the DAG view?
		show_description_on_hover: false, // can be true or false
		give_arrays_a_blank_value: true, // can be true or false // not in use // meant for adding '' to an array // check out line 149 of blinds.js
		// view_node_trigger: 'dblclick', // can be dblclick or click // obsolete
		animate_blinds: false,
		open_new_nodes: true,
		// Keyboard shortcuts. See https://craig.is/killing/mice for options. Currently, we do NOT have functionality to update the mousetrap.bind ings if the user changes their preference without reloading. (That's a TODO).
		search_keycut: 'ctrl+f',
		start_subject_keycut: 'ctrl+a',
		new_node_keycut: 'ctrl+n',
		prefs_keycut: 'ctrl+,',
		save_blind_keycut: 'alt+s',
		edit_save_all_blinds: 'ctrl+s',
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

function setPref(key, val) {
	let dic = {}
	dic[key] = val
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
