"use strict";

var _prototypeProperties = function (child, staticProps, instanceProps) { if (staticProps) Object.defineProperties(child, staticProps); if (instanceProps) Object.defineProperties(child.prototype, instanceProps); };

var _classCallCheck = function (instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } };

define(["jquery", "underscore", "profile", "check-types", "graph"], function ($, _, undefined, is, graph) {

	var blinds = {};

	function string_parser(string_test) {
		//var string_test='Here is a test <img1> and here is a question A tree <<[is]|is not>> an object and the answer is [[10]].Here is <<[exists]| does not exist>> another picture <img2>. Check this one out too [[true]]'

		//var string_test1='There is nothing to replace here'

		var path = "<img src=\"path/to/the/image/";
		var content = "<span class=\"coverup\">";
		var options = "<span class=\"options\">";

		if (string_test.match(/<img[0-9]+>/)) {
			var res1 = string_test.match(/<img[0-9]+>/g);
			for (var i = 0; i < res1.length; i++) {
				x = res1[i].replace("<", "").replace(">", "");
				im_file1 = path.concat(x, ".jpg\">");
				string_test = string_test.replace(res1[i], im_file1);
			}
		}

		if (string_test.match(/\[\[.*\]\]/)) {
			var res2 = string_test.match(/\[\[((?!\]\]).)*\]\]/gi);
			for (var i = 0; i < res2.length; i++) {
				y = res2[i].replace("[[", "").replace("]]", "");
				string_test = string_test.replace(res2[i], content.concat(y, "</span>"));
			}
		}

		if (string_test.match(/<<.*>>/g)) {
			var res3 = string_test.match(/<<((?!>>).)*>>/gi);
			for (var i = 0; i < res3.length; i++) {
				var choice = res3[i].replace("<<", "").replace(">>", "").split("|");
				z = options;
				for (var j = 0; j < choice.length; j++) {
					if (choice[j].startsWith("[")) {
						alert(choice[j]);
						z = z.concat("<span class=\"correct\">", choice[j].replace("[", "").replace("]", ""), "</span>");
					} else {
						z = z.concat("<span>", choice[j], "</span>");
					}
				}
				z = z.concat("</span>");
				string_test = string_test.replace(res3[i], z);
			}
		}
	}

	function init(input) {
		blinds = _.defaults(input, {
			window_id: "blinds",
			keys: undefined, // yes, you can inherit undefined values too
			expand_array_keys: undefined,
			collapse_array_keys: undefined,
			append_keys: undefined,
			chosen: false,
			render: function (x) {
				return x;
			},
			post_render: function (x) {
				return x;
			},
			transform_key: function (x) {
				return x;
			},
			expand_array: false,
			open_empty_blind: true,
			blind_class_conditions: {},
			edit_save_icon: true });

		blinds.$window = $("#" + blinds.window_id);
		delete blinds.window_id;

		blinds.blind_id_counter = 0;
	}

	function open(_ref) {
		var _ref$object = _ref.object;
		var object = _ref$object === undefined ? null : _ref$object;
		var _ref$keys = _ref.keys;
		var keys = _ref$keys === undefined ? blinds.keys : _ref$keys;
		var _ref$expand_array_keys = _ref.expand_array_keys;
		var expand_array_keys = _ref$expand_array_keys === undefined ? blinds.expand_array_keys : _ref$expand_array_keys;
		var _ref$collapse_array_keys = _ref.collapse_array_keys;
		var collapse_array_keys = _ref$collapse_array_keys === undefined ? blinds.collapse_array_keys : _ref$collapse_array_keys;
		var _ref$append_keys = _ref.append_keys;
		var append_keys = _ref$append_keys === undefined ? blinds.append_keys : _ref$append_keys;

		keys = def(keys) ? keys : "own";
		expand_array_keys = def(expand_array_keys) ? expand_array_keys : [];
		collapse_array_keys = def(collapse_array_keys) ? collapse_array_keys : [];
		append_keys = def(append_keys) ? append_keys : [];

		if (object === null) die("Tried to open the blinds with no blinds (object input was null or undefined).");
		blinds.object = object;
		var iterable = keys === "own" ? blinds.object : keys;
		for (var key in iterable) {
			if (is.array(iterable)) key = iterable[key]; // for the keys array, grab the STRINGS, not the INDECIS
			var expand_array = blinds.expand_array && !_.contains(collapse_array_keys, key) || _.contains(expand_array_keys, key);
			if (hasOwnPropertyOrGetter(blinds.object, key)) {
				// nonarrays:
				if (is.not.array(blinds.object[key])) {
					if (blinds.object[key] !== null) {
						_openBlind({
							key: key,
							display_key: key,
							expand_array: false });
					} else if (_.contains(append_keys, key)) {
						_openAppendBlind({
							key: key,
							display_key: key,
							is_one_time_only: true,
							expand_array: false });
					}
				}
				// arrays:
				else {
					// for collapse arrays, show an append when its empty:
					if (!expand_array) {
						if (is.not.emptyArray(blinds.object[key])) {
							_openBlind({
								key: key,
								display_key: key,
								expand_array: false });
						} else if (_.contains(append_keys, key)) {
							_openAppendBlind({
								key: key,
								display_key: key,
								is_one_time_only: true,
								expand_array: false });
						}
					}
					// for other arrays, always show append.
					else {
						_openBlind({ // if the array is empty, this won't actually show a blind.  so no problem here.
							key: key,
							display_key: key,
							expand_array: true });
						_openAppendBlind({
							key: key,
							display_key: key,
							expand_array: true });
					}
				}
			}
		}
		// ASSUMING that when we open a blind, it is always in read mode, then we would run post_render here:
		blinds.post_render();
	}

	function close() {
		// save strings of any opened things (or just startReadMode on them)
		blinds.$window.empty(); // attached triggers and things are automatically removed by jQuery (see http://stackoverflow.com/questions/34189052/if-i-bind-a-javascript-event-to-an-element-then-delete-the-element-what-happen)
		blinds.object = undefined;
	}

	function _openBlind(_ref) {
		var _ref$parent_object = _ref.parent_object;
		var parent_object = _ref$parent_object === undefined ? blinds.object : _ref$parent_object;
		var key = _ref.key;
		var expand_array = _ref.expand_array;
		var display_key = _ref.display_key;
		var $before = _ref.$before;
		// at this point, expand_array represents whether we should expand for THIS key specifically.
		if (expand_array && is.array(blinds.object[key])) {
			var array = blinds.object[key];
			// if( is.emptyArray(array) && blinds.open_empty_blind ) array.push('') // empty arrays get a single empty string element
			_.each(array, function (array_element, index) {
				_openBlind({
					parent_object: blinds.object[key],
					key: index,
					display_key: key,
					expand_array: false,
					$before: $before });
			});
		} else {
			if (blinds.open_empty_blind || blinds.object[key] !== "") {
				// if a blind already exists (check '.blind' key in parent_object), fetch it here
				// otherwise...
				var blind = new Blind({
					parent_object: parent_object,
					key: key,
					display_key: display_key,
					mode: blinds.chosen && is.array(parent_object[key]) ? "chosen" : "standard" });
				_displayBlind(blind, $before);
				_enableRenderToggling(blind);
				return blind;
			}
		}
	}

	function _openAppendBlind(_ref) {
		var key = _ref.key;
		var display_key = _ref.display_key;
		var expand_array = _ref.expand_array;
		var is_one_time_only = _ref.is_one_time_only;

		var parent_object = is.array(blinds.object[key]) && expand_array ? blinds.object[key] : blinds.object;
		var blind = new Blind({
			parent_object: parent_object,
			key: key, // there is no key since there is no value
			display_key: display_key,
			mode: "append" });
		_displayBlind(blind);
		_enableAppending(blind, expand_array, is_one_time_only);
	}

	function _displayBlind(blind, $before) {
		if (def($before)) $before.before(blind.htmlified);else blinds.$window.append(blind.htmlified);
	}

	function _enableRenderToggling(blind) {
		$("#" + blind.id + " " + ".edit-save").click(function () {
			_toggleBlind(blind);
		});
	}

	function _enableAppending(blind, expand_array, is_one_time_only) {
		if (is_one_time_only) {
			// it looks like closure wasn't an issue after all.  once the chosen glitch and the one_time_only glitch is resolved, revert this code to the compact form
			$("#" + blind.id + " " + ".append").click(function () {
				var new_blind = _appendValueOrCollapsedBlind(blind, expand_array);
				_toggleBlind(new_blind);
				$("#" + blind.id).remove();
			});
		} else {
			$("#" + blind.id + " " + ".append").click(function () {
				var new_blind = _appendValueOrCollapsedBlind(blind, expand_array);
				_toggleBlind(new_blind);
			});
		}
	}

	function _toggleBlind(blind) {
		var $this = $("#" + blind.id);
		var $value = $this.children(".value:first");

		blind.toggleState();
		if (blind.state === "read") _startReadMode(blind, $value);
		if (blind.state === "write") _startWriteMode(blind, $value);
	}

	function _appendValueOrCollapsedBlind(blind, expand_array) {
		var $this = $("#" + blind.id);
		var key = undefined;
		if (is.array(blind.parent_object)) {
			if (expand_array) {
				blind.parent_object.push("");
				key = blind.parent_object.length - 1;
			} else {
				die("If the parent object is an array, then it should ALWAYS be expand_array.  Because if it is not expand_array, then the PARENT OBJECT should be the bigger dictionary containing the array instead.");
			}
		} else if (is.array(blind.parent_object[blind.key])) {
			if (!expand_array) {
				key = blind.key // this is the collapse array case
				;
			} else {
				die("Similar to die above, this should not happen.");
			}
		} else {
			blind.parent_object[blind.key] = ""; // for regular nonarray things
			key = blind.key;
		}
		return _openBlind({
			parent_object: blind.parent_object,
			key: key, // needs to be ARRAY key when relevant.  // for non-array, blind.key may do
			display_key: blind.display_key,
			expand_array: false,
			$before: $this });
	}

	function _startReadMode(blind, $value) {
		if (blind.mode === "chosen") {
			(function () {
				var selected_elements = [];
				// grab the options that have the selected property (jQuery)
				$("#" + blind.id + " > .value > .tags").children().each(function () {
					if ($(this).prop("selected")) selected_elements.push($(this).val());
				});
				blind.value = selected_elements;
			})();
		} else if (blind.mode === "standard") {
			$value.prop("contenteditable", false);
			blind.value = $value.html();
		} else die("Unexpected blind mode.");

		$value.html(blind.value_htmlified);
		$("#" + blind.id + " " + ".edit-save").attr("src", "images/edit.svg");
		blinds.post_render();

		$.event.trigger({
			type: "save-node" });
	}

	function _startWriteMode(blind, $value) {
		$value.html(blind.value_htmlified);
		if (blind.mode === "chosen") {
			$("#" + blind.id + " > .value > .tags").chosen({ // this seems to work, as opposed to '#'+blind.id+'.tags'
				inherit_select_classes: true,
				search_contains: true,
				width: "100%"
			});
			// $('.tags').append('<option value="new" selected>NEW</option>')
			// the following might be messing things up.  leave it commented until we need that feature
			$("#" + blind.id + " > .value > .tags").trigger("chosen:updated");
		} else if (blind.mode === "standard") {
			$value.prop("contenteditable", true);
			_setCursor($value);
		} else die("Unexpected blind mode.");

		$("#" + blind.id + " " + ".edit-save").attr("src", "images/save.svg");
	}

	$.fn.selectRange = function (start, end) {
		// see http://stackoverflow.com/questions/499126/jquery-set-cursor-position-in-text-area
		if (typeof end === "undefined") {
			end = start;
		}
		return this.each(function () {
			if ("selectionStart" in this) {
				this.selectionStart = start;
				this.selectionEnd = end;
			} else if (this.setSelectionRange) {
				this.setSelectionRange(start, end);
			} else if (this.createTextRange) {
				var range = this.createTextRange();
				range.collapse(true);
				range.moveEnd("character", end);
				range.moveStart("character", start);
				range.select();
			}
		});
	};

	function _setCursor($contenteditable_container) {
		// set the cursor to the beginning and make it appear
		$contenteditable_container.focus(); // <-- needed to see the blinking cursor
		$contenteditable_container.selectRange(0);
	}

	//////////////////////////// BLIND CLASS ////////////////////////////

	var Blind = (function () {
		function Blind(input) {
			_classCallCheck(this, Blind);

			_.defaults(input, {
				parent_object: undefined,
				key: undefined,
				display_key: undefined,
				mode: "standard", // can be 'standard' or 'chosen' or 'append'
				state: "read" });
			_.extendOwn(this, input);
		}

		_prototypeProperties(Blind, null, {
			id: {
				get: function () {
					if (!def(this._id)) this._id = "Blind-ID-" + (blinds.blind_id_counter++).toString();
					return this._id;
				},
				configurable: true
			},
			value: {
				get: function () {
					// hand over the iterable() (or string) of the BlindValue object value
					if (this.mode === "append") {
						return "Add a new " + this.display_key.singularize() + "!";
					} else {
						return this.parent_object[this.key];
					}
				},
				set: function (new_value) {
					// create a BlindValue object with new_value, or if it already exists, update the obj w/ new_value
					this.parent_object[this.key] = new_value;
				},
				configurable: true
			},
			classes: {
				get: function () {
					var classes = ["blind"];
					if (this.mode === "append") classes.push("blind-append");
					for (var class_name in blinds.blind_class_conditions) {
						var value = blinds.blind_class_conditions[class_name];
						if (is["function"](value)) {
							var bool_func = value;
							if (bool_func(blinds.object, this.display_key, this.key)) classes.push(class_name);
						} else if (is.boolean(value)) {
							var bool = value;
							if (bool) classes.push(class_name);
						}
					}
					return classes;
				},
				configurable: true
			},
			htmlified: {

				// get index() {
				// 	// may not need this //
				// }

				get: function () {
					return "<div id=\"" + this.id + "\" class=\"" + this.classes_htmlified + "\">"
					// + '<span class="key" data-key="'+this.key+'"' + this.index_htmlified + '>' // may not need this info at all!
					 + "<div class=\"key\" data-key=\"" + this.key + "\">" + this.display_key_htmlified + "&nbsp&nbsp" + "</div>" + "<div class=\"value\" " + this.contenteditable_htmlified + ">" + this.value_htmlified + "</div>" + this.icon_htmlified + "</div>";
				},
				configurable: true
			},
			icon_htmlified: {
				get: function () {
					if (this.mode === "append") return "<img class=\"icon append\" src=\"images/add.svg\" />";
					return blinds.edit_save_icon ? "<img class=\"icon edit-save\" src=\"images/" + editOrSave(this.state) + ".svg\" />" : "";
					function editOrSave(state) {
						return state === "read" ? "edit" : "save";
					}
				},
				configurable: true
			},
			display_key_htmlified: {
				get: function () {
					return blinds.render(blinds.transform_key(this.display_key, blinds.object) + ":") // marked wraps this in paragraph tags and NEWLINES. NEWLINES are rendered in HTML as a single space
					;
				},
				configurable: true
			},
			value_htmlified: {
				get: function () {
					var value_string = is.array(this.value) ? this.value.join(", ") : this.value;
					if (this.state === "write") {
						if (this.mode === "chosen") return as_select_html(this.value);else return value_string;
					} else if (this.state === "read") {
						return blinds.render(value_string);
					} else die("Bad state.");
				},
				configurable: true
			},
			classes_htmlified: {
				get: function () {
					return this.classes.join(" ");
				},
				configurable: true
			},
			contenteditable_htmlified: {
				get: function () {
					if (this.state === "read") return "";else if (this.state === "write") return "contenteditable";else die("Bad state.");
				},
				configurable: true
			},
			toggleState: {
				value: function toggleState() {
					if (this.state === "read") this.state = "write";else if (this.state === "write") this.state = "read";else die("Bad state.");
				},
				writable: true,
				configurable: true
			}
		});

		return Blind;
	})();

	//////////////////////////// BLINDVALUE CLASS ////////////////////////////

	var BlindValue = (function () {
		function BlindValue(value) {
			_classCallCheck(this, BlindValue);
		}

		_prototypeProperties(BlindValue, null, {
			"this": {
				get: function () {
					return this.iterable["this"];
				},
				configurable: true
			},
			_iterable: {
				set: function (array) {
					// this could possibly be something other than an array if necessary
					// if an iterable already exists, complain
					// the array can also hold a hidden 'this' key which holds the pointer to the blind value
					this.__iterable = array;
				},
				configurable: true
			},
			iterable: {
				get: function () {
					return this.__iterable;
				},
				configurable: true
			},
			select: {
				value: function select(el) {},
				writable: true,
				configurable: true
			},
			deselect: {
				value: function deselect(el) {},
				writable: true,
				configurable: true
			},
			_append: {
				value: function _append(el, bool) {},
				writable: true,
				configurable: true
			},
			_delete: {
				value: function _delete(el) {},
				writable: true,
				configurable: true
			}
		});

		return BlindValue;
	})();

	////////////////////////////// HELPERS //////////////////////////////
	function as_select_html(array_selected) {
		var client_node_names = graph.nodeNamesList();

		var string = "<select class=\"tags\" multiple>";
		_.each(client_node_names, function (el) {
			string = string + "<option value=\"" + el + "\" " + selected(array_selected, el) + ">" + el + "</option>";
		});
		string = string + "</select>";
		return string;
	}

	function selected(array_selected, el) {
		if (_.contains(array_selected, el)) {
			return "selected";
		} // we set property selected to true, so it's pre-selected
		return "";
	}

	////////////////////////////// EXPORTS //////////////////////////////
	return {
		init: init,
		open: open,
		close: close };
}); // we could grab the jQuery $sel here by using last() (or possibly the return value of append()).  Then we would not need '#'+blind.id to tie the trigger.  But we *may* need blind.id for something else.  That is, resuing blind objects if we wanted to do that for some reason.
// request-node will happen on the server side
// this is how to update chosen after adding more options

// can be 'read' or 'write'

// if string, store it
// if array, map el to [el, true] and store

// if element exists, make sure its true
// otherwise, create it true

// if el exists, make false
// otherwise, create it false

// create it w/ bool value

// we may need this in the future
// end of define

