define(["underscore", "check-types", "profile", "user"], function(_, check, undefined, user) {

/////////////////////////////////// HELPERS ///////////////////////////////////
function _removeParenthesizedThing(string){ // not yet correctly integrated into project
	return string.replace(/\([^\)]*\)/, '');
}

function _removeOneContextFromNames(){ // not yet correctly integrated into project
	// go through nodes and update the displayNames to be the _names with removal (above function)
	_.each(d3AndSVG.nodes, function(node){
		// node.displayName = removeParenthesizedThing( node.name[0] )
	})
	graphAnimation.update()
}

function _showFullContextInNames(){ // not yet correctly integrated into project
	_.each(d3AndSVG.nodes, function(node){
		// node.displayName = node.name[0]
	})
	graphAnimation.update()
}

function _removeLeadingUnderscoresFromKeys(obj) {
	_.each(obj, function(value, key){ if( key[0] === '_' ){
		delete obj[key]
		key = key.substr(1)
		obj[key] = value
	}})
	return obj
}


///////////////////////////////////// MAIN ////////////////////////////////////
class Node {

	constructor(object) {
		_removeLeadingUnderscoresFromKeys(object)
		_.extend(this, object)
		if( this.empty ){
			// then it's an "axiom"...
			this.name = "id: " + this.id
			this.type = "axiom"
			this.description = "No description.  Please fill it in for us!"
		}
	}

	stringify() {
		return "automatic attributes:\n\n" + JSON.stringify(this)
			+ "\n\nspecial attributes:\n\n"
			+ "learned: " + this.learned + "display_name: " + this.display_name
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
		if( !check.string(new_name) ) die('gA_display_name must be a string.')
		this._gA_display_name = new_name
	}

	get gA_display_name() {
		if( def(this._gA_display_name ) ) return this._gA_display_name
		return this.display_name
	}

	// set display_name(string) { // well we may never need to set it, if we check user pref object every time
	// 	if( !check.string(string) ) die("A node's display_name must be a string.")
	// 	this._display_name = string
	// }

	get display_name() {
		switch( user.prefs.display_name_capitalization ){
			case null:
				return this.name
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
				// alert('name is: ' + this.name)
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

