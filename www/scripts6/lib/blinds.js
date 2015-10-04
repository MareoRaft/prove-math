define( ["jquery", "underscore", "profile", "check-types"], function($, _, undefined, check){

let blinds = {}
function init({
			window_id = 'blinds',
			blind_class = 'blind',
			render = x => x,
			transform_key = x => x,
			expand_array = false,
			open_empty_blind = true,
			blind_class_conditions = {},
		}) {
	blinds.$window = $('#' + window_id)
	blinds.render = render
	blinds.transform_key = transform_key
	blinds.blind_class = blind_class
	blinds.expand_array = expand_array
	blinds.open_empty_blind = open_empty_blind
	blinds.blind_class_conditions = blind_class_conditions
}

function open({ object=null, keys='own', expand_array_keys=[], collapse_array_keys=[] }) {
	if( object === null ) die('Tried to open the blinds with no blinds (object input was null or undefined).')
	blinds.object = object
	let iterable = (keys === 'own')? blinds.object: keys
	for( let key in iterable ){
		if( check.array(iterable) ) key = iterable[key] // for the keys array, grab the STRINGS, not the INDECIS
		if( blinds.object.hasOwnProperty(key) ){
			_openBlind({
				key: key,
				expand_array: (blinds.expand_array && !_.contains(collapse_array_keys, key)) || _.contains(expand_array_keys, key),
			})
		}
	}
	_enableDoubleClickRenderToggling() // enables this in general for all blinds
}

function close() {
	// looping through all the divs.... if their state is write...  _endEditMode($key, $value)
	$('.'+blinds.blind_class).each(function(){
		let $key = $(this).children('.key:first')
			let key = $key.attr('data-key')
			let index = $key.attr('data-index')
		let $value = $(this).children('.value:first')
		let state = _getState(key, index)
		if( state === 'write' ) _endEditMode($key, $value) // (but LEAVE the state as write!)
	})
	blinds.$window.html('')
	blinds.object = undefined
}

function _openBlind({ key, expand_array, index }) { // at this point, expand_array represents whether we should expand for THIS key specifically.
	// alert('opening blind')
	// alert('focus: '+JSON.stringify(blinds.object[key])+'   and   index: '+index+' and expand_array: '+expand_array)
	if( expand_array && check.array(blinds.object[key]) ) _.each(blinds.object[key], function(array_element, index) {
		_openBlind({
			key: key,
			expand_array: false,
			index: index,
		})
	})
	else {
		if( !def(index) && check.array(blinds.object[key]) ) blinds.object[key] = blinds.object[key].join(', ') // when expand_array is off, we should join arrays together with commas.
		if( blinds.open_empty_blind || blinds.object[key] !== '' ){
			_displayBlind({
				key: key,
				index: index,
			})
		}
	}
}

function _displayBlind({ key, index }) {
	let value_string = def(index)? blinds.object[key][index]: blinds.object[key]
	if( !def(value_string) || value_string === null) die('Found undefined or null value.  Do you want to show this?')
	let data_index_string = def(index)? 'data-index="'+index+'"': ''
	let class_string = blinds.blind_class
	_.each(blinds.blind_class_conditions, function(bool_func, class_key) {
		if( bool_func(blinds.object, key, index) ) class_string = class_string + ' ' + class_key
	})

	blinds.$window.append(
		'<div class="' + class_string + '">'
			+ '<span class="key" data-key="'+key+'"' + data_index_string + '>'
				+ blinds.render(blinds.transform_key(key, blinds.object) + ':')
			+ '</span>'
			+ ' ' // this space is not actually necessary, as marked wraps the above in paragraph tags and NEWLINES. NEWLINES are rendered in HTML as a single space
			+ '<span class="value">' + blinds.render(value_string) + '</span>'
		+ '</div>'
	)

	let $this = $('.'+blinds.blind_class).last()
	let $key = $this.children('.key:first') // figure out how to get rid of this block here and in close() and in enableDoubleClickRendering. maybe each of these variables can be a function?
		// let key = $key.attr('data-key') // this line is the issue!
		// let index = $key.attr('data-index')
	// let $value = $this.children('.value:first')
	// let state = _getState(key, index)
	// if( state === 'write' ) _startEditMode($key, $value)
}

function _enableDoubleClickRenderToggling() {
	$('.' + blinds.blind_class).dblclick(function(){
		let $key = $(this).children('.key:first')
			let key = $key.attr('data-key')
			let index = $key.attr('data-index')
		let $value = $(this).children('.value:first')
		let state = _getState(key, index)
		if( state === 'read' ){
			_startEditMode($key, $value)
			_setCursor($value)
			blinds.object[_getStateString(key, index)] = 'write'
		}
		else if( state === 'write' ){
			_endEditMode($key, $value)
			blinds.object[_getStateString(key, index)] = 'read'
		}
		else die('Unexpected state "'+state+'".')
	})
}

function _getState(key, index) {
	return blinds.object[_getStateString(key, index)] || 'read' // the first time a $value is double clicked, the corresponding state is undefined.  Here, we default it to 'read'.
}

function _getStateString(key, index) {
	if( _keyHoldsString(key) ){
		return key + '-state'
	}
	else if( _keyHoldsArrayOfStrings(key) ) {
		return key + '-' + index.toString() + '-state'
	}
	else die('Unexpected object[key] type.')
}

function _startEditMode($key, $value) {
	$value.html(_getBlindValueFromObject($key))
	$value.prop('contenteditable', true)
}

function _endEditMode($key, $value) {
	$value.prop('contenteditable', false)
	// take value, STORE IT, then display the render()ed version of it
	_storeBlindValueIntoObject($key, $value) // THIS IS a mistake because it only works if the blind value is a pure string.  we need to protect against accidentally storing the rendered string into here (bad use of _endEditMode).
	$value.html(blinds.render(_getBlindValueFromObject($key)))
}

function _storeBlindValueIntoObject($key, $value) {
	let key = $key.attr('data-key')
	if( _keyHoldsString(key) ){
		blinds.object[key] = $value.html() // store the html string back into the object (save changes for future use)
	}
	else if( _keyHoldsArrayOfStrings(key) ){
		blinds.object[key][$key.attr('data-index')] = $value.html()
	}
	else die('Unexpected value of object: ' + blinds.object[key])
}

function _getBlindValueFromObject($key) { // this is after the blind has been initialized
	let key = $key.attr('data-key')
	if( _keyHoldsString(key) ){
		return blinds.object[key]
	}
	else if( _keyHoldsArrayOfStrings(key) ){
		return blinds.object[key][$key.attr('data-index')]
	}
	else die('Unexpected value of object: ' + blinds.object[key])
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

function _keyHoldsString(key) {
	return check.string(blinds.object[key])
}

function _keyHoldsArrayOfStrings(key) {
	return check.array.of.string(blinds.object[key])
}

return {
	init: init,
	open: open,
	close: close,
}

}) // end of define
