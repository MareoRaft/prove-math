define(["underscore", "check-types", "profile", "user", "graph", "vanilla-notify"], function(_, is, undefined, user, graph, notify) {

/////////////////////////////////// HELPERS ///////////////////////////////////
let type_to_default_importance = {
	'definition': 4,
	'equivdefs': 5,
	'axiom': 4,
	'theorem': 6,
	'example': 2,
	'exercise': 1,
}

function _removeParenthesizedThing(string){ // not yet correctly integrated into project
	return string.replace(/\([^\)]*\)/, '');
}

function _removeOneContextFromNames(){ // not yet correctly integrated into project
	// go through nodes and update the displayNames to be the _names with removal (above function)
	throw 'not yet done'
	_.each(d3AndSVG.nodes, function(node){
		// node.displayName = removeParenthesizedThing( node.name[0] )
	})
	graphAnimation.update()
}

function _showFullContextInNames(){ // not yet correctly integrated into project
	throw 'not yet done'
	_.each(d3AndSVG.nodes, function(node){
		// node.displayName = node.name[0]
	})
	graphAnimation.update()
}

function deepcopy(object){
	return $.extend({}, object)
}

function _removedLeadingUnderscoresFromKeys(obj, exclusions) {
	let new_obj = deepcopy(obj)
	_.each(new_obj, function(value, key){
		if( def(exclusions) && _.contains(exclusions, key) ){
			// pass
		}
		else{
			if( key[0] === '_' ){
				delete new_obj[key]
				key = key.substr(1)
				new_obj[key] = value
			}
		}
	})
	return new_obj
}


///////////////////////////////////// MAIN ////////////////////////////////////
let local_node_id_counter = 0
class Node {

	constructor(object={}) {
		object = _removedLeadingUnderscoresFromKeys(object, ['_id']) // but exclude '_id' key

		// Set some reasonable things for new nodes

		// detect if its "new" or not (although i'm actually not using this info now)
		let is_new = _.isEmpty(object)? true: false


		// set default type if necessary
		if( !('type' in object) || !is.assigned(object['type']) ){
			object['type'] = user.prefs.new_node_default_type
		}
		object['_type'] = object['type']
		delete object['type']

		_.extend(this, object)

		// fill blank or undefined attr values with empty things
		this.fillWithNullAttrs()

		// set default importance if necessary (depending on type)
		if( this.attrs['importance'].value === null ){
			this.attrs['importance'].value = type_to_default_importance[this.type]
		}

		this['_id'] = this.choose_id(this)

		if( this.empty ){
			// then it's an "axiom"...
			alert('emptyy. havent used (or payed attention to) this feature in a while.  If you dont encounter this by January 18, just delete all .empty stuff.')
			this.name = object.id // and remember the ID is generated from this too
		}
	}

	choose_id(object) {
		if ('_id' in object) {
			return object['_id']
		}
		else{
			let id = LOCAL_ID_PREFIX + (local_node_id_counter++).toString()
			return id
		}
	}

	nameAndId() {
		return this.name + ' (NODE-ID is ' + this.id + ')'
	}

	// convenient getters n setters so that other things can treat a node like a normal object and not know the difference
	get type() {
		return this._type
	}
	set type(new_in) {
		if( _.contains(['definition', 'equivdefs', 'axiom', 'theorem', 'example', 'exercise'], new_in) ){
			let old_keys = new Set(this.key_list())
			this._type = new_in
			let new_keys = new Set(this.key_list())
			let obsolete_keys = old_keys.difference(new_keys)
			for( let key of obsolete_keys ){
				delete this.attrs[key]
			}
			this.fillWithNullAttrs()
			// updating the blinds attrs is part of read_mode_action in main.js
		}
		else{
			notify.error({
				text: 'Bad node type.  The node type will not be changed.',
				visibleDuration: 3800,
			})
		}
	}

	// idea: we might create a "reader" function which we pass into blinds.  blinds would call reader(object, key) instead of object[key], and the reader would do what the below does.  Also, a writer.  But for now, this is unneeded.
	get name() {
		if (!def(this.attrs['name'].value) || this.attrs['name'].value === null) return ''
		return this.attrs['name'].value
	}
	set name(new_in) {
		this.attrs['name'].value = new_in
	}
	get examples() {
		return this.attrs['examples'].value
	}
	set examples(new_in) {
		this.attrs['examples'].value = new_in
	}
	get counterexamples() {
		return this.attrs['counterexamples'].value
	}
	set counterexamples(new_in) {
		this.attrs['counterexamples'].value = new_in
	}
	get importance() { // as a STRING
		return this.attrs['importance'].value.toString()
	}
	set importance(new_in) {
		this.attrs['importance'].value = parseInt(new_in)
	}
	get description() {
		return this.attrs['description'].value
	}
	set description(new_in) {
		this.attrs['description'].value = new_in
	}
	get number() {
		return this.attrs['number'].value
	}
	set number(new_in) {
		this.attrs['number'].value = new_in
	}
	get intuitions() {
		return this.attrs['intuitions'].value
	}
	set intuitions(new_in) {
		this.attrs['intuitions'].value = new_in
	}
	get notes() {
		return this.attrs['notes'].value
	}
	set notes(new_in) {
		this.attrs['notes'].value = new_in
	}
	get dependencies() { // the dependency IDs
		return this.attrs['dependencies'].value
	}
	set dependencies(new_in) {
		this.attrs['dependencies'].value = new_in
	}
	get dependency_name_and_ids() {
		return _.map(this.dependencies, function(dependency_id){
			let dependency_node = graph.nodes[dependency_id] // i think it's BAD for the Node module to depend on the graph module

			// FALLBACK: if the node is absent from the graph, return just the ID (see issue #32, #33)
			if( is.undefined(dependency_node) ){
				return dependency_id
			}

			return dependency_node.nameAndId()
		})
	}
	set dependency_name_and_ids(new_in) {
		let re = /.*\(NODE-ID is (.*)\)$/
		let clean_in = _.map(new_in, function(el) {
			if( re.test(el) ){ // if the string matches the regex
				let id = re.exec(el)[1]
				return id
			}
			else {
				return reduce_string(el)
			}
		})
		this.dependencies = clean_in
	}
	get plurals() {
		return this.attrs['plurals'].value
	}
	set plurals(new_in) {
		this.attrs['plurals'].value = new_in
	}
	get negation() {
		return this.attrs['negation'].value
	}
	set negation(new_in) {
		this.attrs['negation'].value = new_in
	}
	get proofs() {
		return this.attrs['proofs'].value
	}
	set proofs(new_in) {
		this.attrs['proofs'].value = new_in
	}

	key_list(user_friendly=false) {
		// construct the keys relevant to the node, depending on its type
		// if node.py is edited, then this needs to be edited to reflect that:
		let keys = ['type', 'number', 'name', 'description', 'intuitions', 'notes', 'examples', 'counterexamples']

		// add keys specific to certain node types
		if( this.type === 'axiom' ) pushArray(keys, ['plurals', 'negation'])
		else if( this.type === 'definition') pushArray(keys, ['plurals', 'negation'])
		else if( this.type === 'equivdefs') pushArray(keys, ['plurals', 'negation', 'proofs'])
		else if( this.type === 'theorem' ) pushArray(keys, ['proofs'])
		else if( this.type === 'example' ) pushArray(keys, ['proofs'])
		else if( this.type === 'exercise' ) pushArray(keys, ['proofs'])
		else die('Node has bad type: '+this.type)

		// add remaining keys (not added up top because we want them to be in a specific order)
		let deps_key = (user_friendly)? 'dependency_name_and_ids': 'dependencies'
		pushArray(keys, ['importance', deps_key])

		return keys
	}

	fillWithNullAttrs() {
		if (!('attrs' in this)) this.attrs = {}
		let keys = this.key_list()

		_.each(keys, function(key){
			if(key !== 'type') {
				this.fillWithNullAttr(key)
			}
		}.bind(this))
	}

	fillWithNullAttr(attr_name) {
		let key = attr_name
		if (!(key in this.attrs)) this.attrs[key] = {}
		if (!('value' in this.attrs[key]) || !def(this.attrs[key])) {
			// for a plural attr, set to []
			if( _.contains(["synonyms", "plurals", "dependencies", "examples", "counterexamples", "intuitions", "notes", "proofs"], key) ){
				if (key === 'dependencies') {
					this.attrs[key].value = [] // patch for dependencies for below convenience
				}
				else {
					this.attrs[key].value = [''] // this is a convenience // was []
				}
			}
			// for a singular attr, set to null
			else{
				if (key === 'importance') {
					this.attrs[key].value = 4 // patch for importance for below convenience
				}
				else {
					this.attrs[key].value = '' // this is a convenience // was null
				}
			}
		}
	}

	dict() {
		let dictionary = {}
		_.each(this, function(value, key) {
			if( this.hasOwnProperty(key) && !_.contains(["index", "weight", "x", "y", "px", "py", "fixed", "_name", "_id"], key) ) {
				dictionary[key] = this[key]
			}
		}.bind(this))
		dictionary["_id"] = this.id // for the server-side
		return dictionary
	}

	stringify() {
		return "automatic attributes:\n\n" + JSON.stringify(this)
			+ "\n\nspecial attributes:"
			+ "\n\nlearned: " + this.learned
			+ "\ndisplay_name: " + this.display_name
			+ "\nid: " + this.id
	}

	alert() {
		notify.info({
			text: this.stringify(),
		})
	}

	set learned(bool) {
		if( bool === true ) user.learnNode(this)
		else if( bool === false ) user.unlearnNode(this)
		else die('You can only set node.learned to a boolean value.')
	}
	get learned() {
		return user.hasLearned(this)
	}

	set gA_display_name(new_name) {
		if( !is.string(new_name) ) die('gA_display_name must be a string.')
		this._gA_display_name = new_name
	}
	get gA_display_name() {
		if( def(this._gA_display_name ) ) return this._gA_display_name
		return this.display_name
	}

	get id() {
		return this._id
	}

	get display_name() {
		if( user.prefs.display_number_instead_of_name && is.nonEmptyString(this.number) ){
			return this.number
		}
		switch( user.prefs.display_name_capitalization ){
			case null:
				return this.name
			case "lower":
				return this.name.toLowerCase()
			case "sentence":
				return this.name.capitalizeFirstLetter()
			case "title":
				// for each word in _display_name, capitalize it unless it's in the small words list
				let small_words_list = [
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
				let display_name = this.name.replace(/\b\w+\b/g, function(match){
					if( !_.contains(small_words_list, match) ){
						match = match.capitalizeFirstLetter()
					}
					return match
				})
				// first and last word must be capitalized always!!!
				display_name = display_name.capitalizeFirstLetter()
				display_name = display_name.replace(/\b\w+\b$/g, match => match.capitalizeFirstLetter())
				return display_name
			default:
				die('Unrecognized display_name_capitalization preference value "'+user.prefs.display_name_capitalization+'".')
		}
	}

	as_printable_html(render_content_func) {
		let node_dict = this.dict()
		// keys to display
		// 'type', 'number', 'name', 'description', 'synonyms', 'plurals', 'notes', 'intuitions', 'examples', 'counterexamples', 'negation', 'proofs', 'importance'
		let keys = ['type', 'name', 'description', 'notes', 'intuitions', 'examples', 'counterexamples', 'proofs']
		let string = ''
		string += '$\\begingroup$' // start scope
		for (let key of keys) {
			if (!(key in node_dict['attrs'])) {
				continue
			}
			let value = node_dict['attrs'][key]['value']
			string = string + '<h4>' + key + '</h4>'
			string = string + value
		}
		string += '$\\endgroup$' // end scope
		string = render_content_func(string)
		// post render?
		return string
	}

}

return Node

}) // end of define

