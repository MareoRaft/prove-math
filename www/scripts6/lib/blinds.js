define( ["jquery", "underscore", "profile", "check-types"], function($, _, undefined, check){

let blinds = {}
function init(input) {
	blinds = _.defaults(input, {
		window_id: 'blinds',
		keys: undefined, // yes, you can inherit undefined values too
		expand_array_keys: undefined,
		collapse_array_keys: undefined,
		chosen: false,
		render: x => x,
		transform_key: x => x,
		expand_array: false,
		open_empty_blind: true,
		blind_class_conditions: {},
	})

	blinds.$window = $('#' + blinds.window_id)
	delete blinds.window_id

	blinds.blind_id_counter = 0
}

function open({
			object = null,
			keys = blinds.keys,
			expand_array_keys = blinds.expand_array_keys,
			collapse_array_keys = blinds.collapse_array_keys,
		}) {
	keys = def(keys)? keys: 'own'
	expand_array_keys = def(expand_array_keys)? expand_array_keys: []
	collapse_array_keys = def(collapse_array_keys)? collapse_array_keys: []

	if( object === null ) die('Tried to open the blinds with no blinds (object input was null or undefined).')
	blinds.object = object
	let iterable = (keys === 'own')? blinds.object: keys
	for( let key in iterable ){
		if( check.array(iterable) ) key = iterable[key] // for the keys array, grab the STRINGS, not the INDECIS
		if( blinds.object.hasOwnProperty(key) ){
			_openBlind({
				key: key,
				display_key: key,
				expand_array: (blinds.expand_array && !_.contains(collapse_array_keys, key)) || _.contains(expand_array_keys, key),
			})
		}
	}
}

function close() {
	// save strings of any opened things (or just startReadMode on them)
	blinds.$window.html('')
	blinds.object = undefined
	// clear jquery id double-click triggers?
}

function _openBlind({ parent_object=blinds.object, key, expand_array, display_key }) { // at this point, expand_array represents whether we should expand for THIS key specifically.
	if( expand_array && check.array(blinds.object[key]) ) _.each(blinds.object[key], function(array_element, index) {
		_openBlind({
			parent_object: blinds.object[key],
			key: index,
			display_key: key,
			expand_array: false,
		})
	})
	else {
		if( blinds.open_empty_blind || blinds.object[key] !== '' ){
			// if a blind already exists (check '.blind' key in parent_object), fetch it here
			// otherwise...
			let blind = new Blind({
				parent_object: parent_object,
				key: key,
				display_key: display_key,
				mode: (blinds.chosen && check.array(parent_object[key]) )? 'chosen': 'standard',
			})
			_displayBlind(blind)
			_enableDoubleClickRenderToggling(blind)
		}
	}
}

function _displayBlind(blind) {
	blinds.$window.append(blind.htmlified) // we could grab the jQuery $sel here by using last() (or possibly the return value of append()).  Then we would not need '#'+blind.id to tie the trigger.  But we *may* need blind.id for something else.  That is, resuing blind objects if we wanted to do that for some reason.
}

function _enableDoubleClickRenderToggling(blind) {
	$('#'+blind.id).dblclick(function(){ _toggleBlindGiven$selected(blind, $(this)) })
}

function _toggleBlindGiven$selected(blind, $this) {
	let $key = $this.children('.key:first')
		let key = $key.attr('data-key')
		let index = $key.attr('data-index')
	let $value = $this.children('.value:first')

	blind.toggleState()
	if(blind.state === 'read') _startReadMode(blind, $value)
	if(blind.state === 'write') _startWriteMode(blind, $value)
}

function _startReadMode(blind, $value) {
	if( blind.mode === 'chosen' ){
		let selected_elements = []
		// grab the options that have the selected property (jQuery)
		$('#'+blind.id+' '+'.chosen').children().each(function(){
			if( $(this).prop('selected') ) selected_elements.push($(this).val())
		})
		// put them in an array and give it to blind.value
		blind.value = selected_elements
		// alert('partially implemented')
	}
	else if( blind.mode === 'standard' ){
		$value.prop('contenteditable', false)
		blind.value = $value.html()
	}
	else die('Unexpected blind mode.')



	$value.html(blind.value_htmlified)
}

function _startWriteMode(blind, $value) {
	$value.html(blind.value_htmlified)
	if( blind.mode === 'chosen' ){
		$('.chosen').chosen({ width: '100%' }) // this should probably be moved to the end of open()
		// can we add more options after the fact?
		// $('.chosen').append('<option value="new" selected>NEW</option>')
		$('.chosen').trigger('chosen:updated') // this is how to update chosen after adding more options

	}
	else if( blind.mode === 'standard' ){
		$value.prop('contenteditable', true)
		_setCursor($value)
	}
	else die('Unexpected blind mode.')
}

function _setCursor($contenteditable_container) {
	// set the cursor to the beginning and make it appear
	$contenteditable_container.focus() // <-- needed for Firefox
	let range = document.createRange()
	let sel = window.getSelection()
	range.setStart($contenteditable_container.get(0).childNodes[0], 0); // line 0, character 0
	range.collapse(true)
	sel.removeAllRanges()
	sel.addRange(range)
}

//////////////////////////// BLIND CLASS ////////////////////////////
class Blind {

	constructor(input) {
		_.defaults(input, {
			parent_object: undefined,
			key: undefined,
			display_key: undefined,
			mode: 'standard', // can be 'standard' or 'chosen'
			state: 'read', // can be 'read' or 'write'
		})
		_.extendOwn(this, input)
	}

	get id() {
		if( !def(this._id) ) this._id = 'Blind-ID-' + (blinds.blind_id_counter++).toString()
		return this._id
	}

	get value() {
		return this.parent_object[this.key]
	}

	set value(new_value) {
		this.parent_object[this.key] = new_value
	}

	get classes() {
		let classes = []
		for( let class_name in blinds.blind_class_conditions ){
			let value = blinds.blind_class_conditions[class_name]
			if( check.function(value) ){
				let bool_func = value
				if( bool_func(blinds.object, this.display_key, this.key) ) classes.push(class_name)
			}
			else if( check.boolean(value) ){
				let bool = value
				if( bool ) classes.push(class_name)
			}
		}
		return classes
	}

	// get index() {
	// 	// may not need this
	// }

	get htmlified() {
		return	'<div id="' + this.id + '" class="' + this.classes_htmlified + '">'
					// + '<span class="key" data-key="'+this.key+'"' + this.index_htmlified + '>' // may not need this info at all!
					+ '<span class="key" data-key="'+this.key+'">'
						+ this.display_key_htmlified
					+ '</span>'
					+ ' ' // this space is not actually necessary, as marked wraps the above in paragraph tags and NEWLINES. NEWLINES are rendered in HTML as a single space
					+ '<span class="value" ' + this.contenteditable_htmlified + '>'
						+ this.value_htmlified
					+ '</span>'
			+ '</div>'
	}

	get display_key_htmlified() {
		return blinds.render(blinds.transform_key(this.display_key, blinds.object) + ':')
	}

	get value_htmlified() {
		let value_string = check.array(this.value)? this.value.join(', '): this.value
		if(this.state === 'write'){
			if( this.mode === 'chosen' ) return as_select_html(this.value)
			else return value_string
		}
		else if(this.state === 'read') return blinds.render(value_string)
		else die('Bad state.')
	}

	get classes_htmlified() {
		return this.classes.join(' ')
	}

	get contenteditable_htmlified() {
		if(this.state === 'read') return ''
		else if(this.state === 'write') return 'contenteditable'
		else die('Bad state.')
	}

	toggleState() {
		if(this.state === 'read') this.state = 'write'
		else if(this.state === 'write') this.state = 'read'
		else die('Bad state.')
	}
}

////////////////////////////// HELPERS //////////////////////////////
function as_select_html(array) {
	// alert(check.array(array))
	let string = '<select class="chosen" multiple>'
	_.each(array, function(el){
		// alert(el) // you know, there is something fishy about this array!  it has this weird extra "true" in it and maybe a function?
		string = string + '<option value="'+el+'" selected>'+el+'</option>' // we set property selected to true, so that everything is pre-selected
		// we can add other options to the list by grabbing other node names, but don't use selected for these
	})
	string = string + '</select>'
	return string
}

////////////////////////////// EXPORTS //////////////////////////////
return {
	init: init,
	open: open,
	close: close,
}

}) // end of define
