define(["underscore", "check-types", "profile", "user"], function(_, is, undefined, user) {

/////////////////////////////////// HELPERS ///////////////////////////////////
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

function _removedLeadingUnderscoresFromKeys(obj) {
	let new_obj = deepcopy(obj)
	_.each(new_obj, function(value, key){ if( key[0] === '_' ){
		delete new_obj[key]
		key = key.substr(1)
		new_obj[key] = value
	}})
	return new_obj
}


///////////////////////////////////// MAIN ////////////////////////////////////
class Node {

	constructor(object={}) {
		object = _removedLeadingUnderscoresFromKeys(object)
		_.defaults(object, {
			type: 'axiom', // not yet addressed
		})
		object['_id'] = object['id']
		delete object['id']
		_.extend(this, object)
		// TODO: SEE IF THE DICT ID IS SET OR NOT
		if( this.empty ){
			// then it's an "axiom"...
			this.name = object.id // and remember the ID is generated from this too
		}
		this.fillWithNullKeys()
	}

	// convenient getters n setters so that other things can treat a node like a normal object and not know the difference
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
	get dependencies() {
		return this.attrs['dependencies'].value
	}
	set dependencies(new_in) {
		this.attrs['dependencies'].value = new_in
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

	get key_list() {
		// construct the keys relevant to the node, depending on its type
		// if node.py is edited, then this needs to be edited to reflect that:
		let keys = ['name', 'importance', 'description', 'intuitions', 'notes', 'dependencies', 'examples', 'counterexamples']
		if( this.type === 'axiom' ) pushArray(keys, ['plurals', 'negation'])
		else if( this.type === 'definition') pushArray(keys, ['plurals', 'negation'])
		else if( this.type === 'theorem' ) pushArray(keys, ['proofs'])
		else if( this.type === 'exercise' ) pushArray(keys, ['proofs'])
		else die('Node has no type.')
		return keys
	}

	fillWithNullKeys() {
		let keys = this.key_list
		let node = this // this changes within the anonymous function
		_.each(keys, function(key) {
			if( !key in node || !def(node[key]) ) {
				// for plural things, set to []
				if( _.contains(["synonyms", "plurals", "dependencies", "examples", "counterexamples", "intuitions", "notes", "proofs"], key) ){
					node.attrs[key].value = []
				}
				// for singular things, set to null
				else{
					node.attrs[key].value = null
				}
			}
		})
	}

	dict() {
		let dictionary = {}
		let node = this
		_.each(this, function(value, key) { if( node.hasOwnProperty(key) && !_.contains(["index", "weight", "x", "y", "px", "py", "fixed", "_name", "_id"], key) ) {
			dictionary[key] = node[key]
		}})
		dictionary["_id"] = node.id // for the server-side
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
		alert(this.stringify())
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
		if( this._id !== null && this._id !== '' ) return this._id
		else if( this.name !== null && this.name !== '' ) return reduce_string(this.name)
		else die('not sure what the id should be')
	}

	get display_name() {
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
}

return Node

}) // end of define

