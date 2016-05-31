"use strict";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

define(["underscore", "check-types", "profile", "user"], function (_, is, undefined, user) {

	/////////////////////////////////// HELPERS ///////////////////////////////////
	function _removeParenthesizedThing(string) {
		// not yet correctly integrated into project
		return string.replace(/\([^\)]*\)/, '');
	}

	function _removeOneContextFromNames() {
		// not yet correctly integrated into project
		// go through nodes and update the displayNames to be the _names with removal (above function)
		_.each(d3AndSVG.nodes, function (node) {
			// node.displayName = removeParenthesizedThing( node.name[0] )
		});
		graphAnimation.update();
	}

	function _showFullContextInNames() {
		// not yet correctly integrated into project
		_.each(d3AndSVG.nodes, function (node) {
			// node.displayName = node.name[0]
		});
		graphAnimation.update();
	}

	function _removeLeadingUnderscoresFromKeys(obj) {
		_.each(obj, function (value, key) {
			if (key[0] === '_') {
				delete obj[key];
				key = key.substr(1);
				obj[key] = value;
			}
		});
		return obj;
	}

	///////////////////////////////////// MAIN ////////////////////////////////////

	var Node = function () {
		function Node() {
			var object = arguments.length <= 0 || arguments[0] === undefined ? {} : arguments[0];

			_classCallCheck(this, Node);

			_removeLeadingUnderscoresFromKeys(object);
			_.defaults(object, {
				type: 'axiom',
				importance: 5
			});
			_.extend(this, object);
			if (this.empty) {
				// then it's an "axiom"...
				this.name = object.id; // and remember the ID is generated from this too
			}
			this.fillWithNullKeys();
		}

		_createClass(Node, [{
			key: "fillWithNullKeys",
			value: function fillWithNullKeys() {
				// if node.py is edited, then this needs to be edited to reflect that:
				var keys = ['name', 'id', 'type', 'importance', 'description', 'intuitions', 'dependencies', 'examples', 'counterexamples'];
				if (this.type === 'axiom') pushArray(keys, ['synonyms', 'plurals', 'notes', 'negation']);else if (this.type === 'definition') pushArray(keys, ['synonyms', 'plurals', 'notes', 'negation']);else if (this.type === 'theorem') pushArray(keys, ['proofs']);else if (this.type === 'exercise') pushArray(keys, ['proofs']);

				var node = this; // this changes within the anonymous function
				_.each(keys, function (key) {
					if (!key in node || !def(node[key])) {
						if (_.contains(["synonyms", "plurals", "dependencies"], key)) node[key] = [];else node[key] = null;
					}
				});
			}
		}, {
			key: "dict",
			value: function dict() {
				var dictionary = {};
				var node = this;
				_.each(this, function (value, key) {
					if (node.hasOwnProperty(key) && !_.contains(["index", "weight", "x", "y", "px", "py", "fixed", "_name", "_id"], key)) {
						dictionary[key] = node[key];
					}
				});
				dictionary.name = node._name;
				dictionary.id = node.id;
				return dictionary;
			}
		}, {
			key: "stringify",
			value: function stringify() {
				return "automatic attributes:\n\n" + JSON.stringify(this) + "\n\nspecial attributes:" + "\n\nlearned: " + this.learned + "\ndisplay_name: " + this.display_name + "\nname: " + this.name + "\nid: " + this.id;
			}
		}, {
			key: "alert",
			value: function (_alert) {
				function alert() {
					return _alert.apply(this, arguments);
				}

				alert.toString = function () {
					return _alert.toString();
				};

				return alert;
			}(function () {
				alert(this.stringify());
			})
		}, {
			key: "learned",
			set: function set(bool) {
				if (bool === true) user.learnNode(this);else if (bool === false) user.unlearnNode(this);else die('You can only set node.learned to a boolean value.');
			},
			get: function get() {
				return user.hasLearned(this);
			}
		}, {
			key: "gA_display_name",
			set: function set(new_name) {
				if (!is.string(new_name)) die('gA_display_name must be a string.');
				this._gA_display_name = new_name;
			},
			get: function get() {
				if (def(this._gA_display_name)) return this._gA_display_name;
				return this.display_name;
			}

			// set display_name(string) { // well we may never need to set it, if we check user pref object every time
			// 	if( !is.string(string) ) die("A node's display_name must be a string.")
			// 	this._display_name = string
			// }

		}, {
			key: "id",
			set: function set(new_id) {
				if (this.name === null || this.name === '') this._id = new_id;
			},
			get: function get() {
				if (this.name !== null && this.name !== '') return reduce_string(this.name);else if (this._id !== null && this._id !== '') return this._id;else return '';
			}
		}, {
			key: "name",
			set: function set(new_name) {
				this._name = new_name;
			},
			get: function get() {
				if (!def(this._name) || this._name === null) return '';
				return this._name;
			}
		}, {
			key: "display_name",
			get: function get() {
				switch (user.prefs.display_name_capitalization) {
					case null:
						return this.name;
					case "lower":
						return this.name.toLowerCase();
					case "sentence":
						return this.name.capitalizeFirstLetter();
					case "title":
						// for each word in _display_name, capitalize it unless it's in the small words list
						var small_words_list = [
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
						'at', 'around', 'by', 'after', 'along', 'for', 'from', 'in', 'into', 'minus', 'of', 'on', 'per', 'plus', 'qua', 'sans', 'since', 'to', 'than', 'times', 'up', 'via', 'with', 'without'];
						var display_name = this.name.replace(/\b\w+\b/g, function (match) {
							if (!_.contains(small_words_list, match)) {
								match = match.capitalizeFirstLetter();
							}
							return match;
						});
						// first and last word must be capitalized always!!!
						display_name = display_name.capitalizeFirstLetter();
						display_name = display_name.replace(/\b\w+\b$/g, function (match) {
							return match.capitalizeFirstLetter();
						});
						return display_name;
					default:
						die('Unrecognized display_name_capitalization preference value "' + user.prefs.display_name_capitalization + '".');
				}
			}
		}]);

		return Node;
	}();

	return Node;
}); // end of define