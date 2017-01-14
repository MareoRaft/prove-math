define( ["jquery", "underscore", "profile", "check-types", "graph", "mousetrap", "user"], function($, _, undefined, is, graph, mousetrap, user){

//////////////////////////// HELPERS ////////////////////////////
$.fn.selectRange = function(start, end) {
// see http://stackoverflow.com/questions/499126/jquery-set-cursor-position-in-text-area
	if (typeof end === 'undefined') {
		end = start
	}
	return this.each(function() {
		if('selectionStart' in this) {
			this.selectionStart = start
			this.selectionEnd = end
		} else if(this.setSelectionRange) {
			this.setSelectionRange(start, end)
		} else if(this.createTextRange) {
			var range = this.createTextRange()
			range.collapse(true)
			range.moveEnd('character', end)
			range.moveStart('character', start)
			range.select()
		}
	})
}

//////////////////////////// BLINDS CLASS ////////////////////////////
class Blinds {

	constructor(input) {
		let options = _.defaults(input, {
			window_id: 'blinds',
			keys: undefined, // yes, you can inherit undefined values too
			expand_array_keys: undefined,
			collapse_array_keys: undefined,
			append_keys: undefined,
			chosen: false,
			render: x => x,
			post_render: x => x,
			transform_key: x => x,
			expand_array: false,
			open_empty_blind: true,
			blind_class_conditions: {},
			read_mode_action: function(){},
			edit_save_icon: true,
			blinds: [], // stores created blinds, so we can fetch them later
			open_blind_default_state: 'read',
		})
		_.extend(this, options)

		this.$window = $('#' + this.window_id)
		delete this.window_id

		this.blind_id_counter = 0 // this would fail in the future if we allow more than one Blinds to be used simultaneously.  We might need to add an ID for the specific instance of blinds.

		// enable toggleBlinds keycut
		mousetrap.bind(user.prefs.edit_save_all_blinds, function(){
			this._toggleBlinds()
			return false
		}.bind(this))
	}

	open({
				object = null,
				keys = this.keys,
				expand_array_keys = this.expand_array_keys,
				collapse_array_keys = this.collapse_array_keys,
				append_keys = this.append_keys,
			}) {
		if( object === null ) die('Tried to open the blinds with no object to open (object input was null or undefined).')
		this.object = object
		keys = def(keys)? keys: 'own'
		expand_array_keys = def(expand_array_keys)? expand_array_keys: []
		collapse_array_keys = def(collapse_array_keys)? collapse_array_keys: []
		append_keys = def(append_keys)? append_keys: []

		let iterable = (keys === 'own')? this.object: keys
		for( let key in iterable ){
			if( is.array(iterable) ) key = iterable[key] // for the keys array, grab the STRINGS, not the INDECIS
			let expand_array = (this.expand_array && !_.contains(collapse_array_keys, key)) || _.contains(expand_array_keys, key)
			if( hasOwnPropertyOrGetter(this.object, key) ){
				// nonarrays:
				if( is.not.array(this.object[key]) ){
					if( this.object[key] !== null ) {
						this._openBlind({
							key: key,
							display_key: key,
							expand_array: false,
						})
					}
					else if( _.contains(append_keys, key) ) {
						this._openAppendBlind({
							key: key,
							display_key: key,
							is_one_time_only: true,
							expand_array: false,
						})
					}
				}
				// arrays:
				else {
					// for collapse arrays, show an append when its empty:
					if( !expand_array ){
						if( is.not.emptyArray(this.object[key]) ) {
							this._openBlind({
								key: key,
								display_key: key,
								expand_array: false,
							})
						}
						else if( _.contains(append_keys, key) ) {
							this._openAppendBlind({
								key: key,
								display_key: key,
								is_one_time_only: true,
								expand_array: false,
							})
						}
					}
					// for other arrays, always show append.
					else{
						this._openBlind({ // if the array is empty, this won't actually show a blind.  so no problem here.
							key: key,
							display_key: key,
							expand_array: true,
						})
						this._openAppendBlind({
							key: key,
							display_key: key,
							expand_array: true,
						})
					}
				}
			}
		}
		// ASSUMING that when we open a blind, it is always in read mode, then we would run post_render here:
		// TODO -- check this isn't messing things up, when we start blinds in edit mode.
		this.post_render()
	}

	close() {
		// save strings of any opened things (or just startReadMode on them)
		this.$window.empty() // attached triggers and things are automatically removed by jQuery (see http://stackoverflow.com/questions/34189052/if-i-bind-a-javascript-event-to-an-element-then-delete-the-element-what-happen)
		this.blinds = []
		this.object = undefined
	}

	_openBlind({ parent_object=this.object, key, expand_array, display_key, $before }) { // at this point, expand_array represents whether we should expand for THIS key specifically.
		if( expand_array && is.array(this.object[key]) ) {
			let array = this.object[key]
			// if( is.emptyArray(array) && this.open_empty_blind ) array.push('') // empty arrays get a single empty string element
			for( let index in array ){
				this._openBlind({
					parent_object: this.object[key],
					key: index,
					display_key: key,
					expand_array: false,
					$before: $before,
				})
			}
		}
		else {
			if( this.open_empty_blind || this.object[key] !== '' ){
				// if a blind already exists (check '.blind' key in parent_object), fetch it here
				// otherwise...
				let blind = new Blind({
					blinds: this,
					parent_object: parent_object,
					key: key,
					display_key: display_key,
					mode: (this.chosen && is.array(parent_object[key]) )? 'chosen': 'standard',
					state: this.open_blind_default_state,
				})
				this._displayBlind(blind, $before)
				this._enableRenderToggling(blind)
				return blind
			}
		}
	}

	_openAppendBlind({ key, display_key, expand_array, is_one_time_only }) {
		let parent_object = (is.array(this.object[key]) && expand_array)? this.object[key]: this.object
		let blind = new Blind({
			blinds: this,
			parent_object: parent_object,
			key: key, // there is no key since there is no value
			display_key: display_key,
			mode: 'append',
		})
		this._displayBlind(blind)
		this._enableAppending(blind, expand_array, is_one_time_only)
	}

	_displayBlind(blind, $before) {
		if( def($before) ) $before.before(blind.htmlified)
		else this.$window.append(blind.htmlified) // we could grab the jQuery $sel here by using last() (or possibly the return value of append()).  Then we would not need '#'+blind.id to tie the trigger.  But we *may* need blind.id for something else.  That is, reusing blind objects if we wanted to do that for some reason.
	}

	_enableRenderToggling(blind) {
		$('#'+blind.id+' '+'.edit-save').click(function(){
			this._toggleBlind(blind)
		}.bind(this))
		// the below only works for the saving direction, since the div can't really be in focus otherwise
		$mousetrap('#'+blind.id+' '+'.value').bind(user.prefs.save_blind_keycut, function(){
			this._toggleBlind(blind)
		}.bind(this))
	}

	_enableAppending(blind, expand_array, is_one_time_only) {
		if( is_one_time_only ){ // it looks like closure wasn't an issue after all.  once the chosen glitch and the one_time_only glitch is resolved, revert this code to the compact form
			$('#'+blind.id+' '+'.append').click(function(){
				let new_blind = this._appendValueOrCollapsedBlind(blind, expand_array)
				this._toggleBlind(new_blind)
				$('#'+blind.id).remove()
			}.bind(this))
		}
		else{
			$('#'+blind.id+' '+'.append').click(function(){
				let new_blind = this._appendValueOrCollapsedBlind(blind, expand_array)
				this._toggleBlind(new_blind)
			}.bind(this))
		}
	}

	_toggleBlind(blind) {
		let $this = $('#'+blind.id)
		let $value = $this.children('.value:first')

		blind.toggleState()
		if(blind.state === 'read') this._startReadMode(blind, $value)
		if(blind.state === 'write') this._startWriteMode(blind, $value)
	}

	_toggleBlinds() {
		// we go through the blinds backwards, so that the cursor will end up focused on the FIRST blind.
		for (let i = this.blinds.length - 1; i >= 0; i--) {
			let blind = this.blinds[i]
			if( blind.mode !== 'append' ){
				this._toggleBlind(blind)
			}
		}
	}

	_appendValueOrCollapsedBlind(blind, expand_array) {
		let $this = $('#'+blind.id)
		let key = undefined
		if( is.array(blind.parent_object) ){
			if( expand_array ){
				blind.parent_object.push('')
				key = blind.parent_object.length - 1
			}
			else{
				die('If the parent object is an array, then it should ALWAYS be expand_array.  Because if it is not expand_array, then the PARENT OBJECT should be the bigger dictionary containing the array instead.')
			}
		}
		else if( is.array(blind.parent_object[blind.key]) ){
			if( !expand_array ){
				key = blind.key // this is the collapse array case
			}
			else{
				die('Similar to die above, this should not happen.')
			}
		}
		else {
			blind.parent_object[blind.key] = '' // for regular nonarray things
			key = blind.key
		}
		return this._openBlind({
			parent_object: blind.parent_object,
			key: key, // needs to be ARRAY key when relevant.  // for non-array, blind.key may do
			display_key: blind.display_key,
			expand_array: false,
			$before: $this,
		})
	}

	_startReadMode(blind, $value) { // save
		if( blind.mode === 'chosen' ){
			let selected_elements = []
			// grab the options that have the selected property (jQuery)
			$('#'+blind.id+' > .value > .tags').children().each(function(){
				if( $(this).prop('selected') ) selected_elements.push($(this).val())
			})
			blind.value = selected_elements
		}
		else if( blind.mode === 'standard' ){
			$value.prop('contenteditable', false)
			blind.value = $value.html()
		}
		else die('Unexpected blind mode.')

		$value.html(blind.value_htmlified)
		$('#'+blind.id+' '+'.edit-save').attr('src', 'images/edit.svg')
		this.post_render()

		if( is.function(this.read_mode_action) ){
			this.read_mode_action(blind.value, blind.key, blind.parent_object)
		}
		else{
			die('A read mode action must be a function.')
		}
	}

	_startWriteMode(blind, $value) { // edit
		$value.html(blind.value_htmlified)
		// TODO: MAYBE THIS CHOSEN STUFF SHOULD BELONG SOMEWHERE ELSE.  If a blind is created in WRITE mode to BEGIN with, this doesn't run.  Perhaps it's an organizational mistake?  Otherwise, we can cheat by having even 'write' mode blinds start in read mode, but then run _startWriteMode immediately.  not advised.
		if( blind.mode === 'chosen' ){
			$('#'+blind.id+' > .value > .tags').chosen({ // this seems to work, as opposed to '#'+blind.id+'.tags'
				inherit_select_classes: true,
				search_contains: true,
				width: '100%'
			})
			// $('.tags').append('<option value="new" selected>NEW</option>')
			// the following might be messing things up.  leave it commented until we need that feature
			$('#'+blind.id+' > .value > .tags').trigger('chosen:updated') // this is how to update chosen after adding more options

		}
		else if( blind.mode === 'standard' ){
			$value.prop('contenteditable', true)
			this._setCursor($value)
		}
		else die('Unexpected blind mode.')

		$('#'+blind.id+' '+'.edit-save').attr('src', 'images/save.svg')
	}

	_setCursor($contenteditable_container) {
		// set the cursor to the beginning and make it appear
		$contenteditable_container.focus() // <-- needed to see the blinking cursor
		$contenteditable_container.selectRange(0)
	}
}

//////////////////////////// BLIND CLASS ////////////////////////////
class Blind {

	constructor(input) {
		_.defaults(input, {
			parent_object: undefined,
			key: undefined,
			display_key: undefined,
			mode: 'standard', // can be 'standard' or 'chosen' or 'append'
			state: 'read', // can be 'read' or 'write'
		})
		_.extendOwn(this, input)
		// verify that a blinds object was attached
		if( !('blinds' in this) ) die('No Blinds object attached to this little Blind object :)')
		// add self to list of blinds in the Blinds object
		this.blinds.blinds.push(this)
	}

	get id() {
		if( !def(this._id) ) this._id = 'Blind-ID-' + (this.blinds.blind_id_counter++).toString()
		return this._id
	}

	get value() {
		// hand over the iterable() (or string) of the BlindValue object value
		if( this.mode === 'append' ){
			return 'Add a new ' + this.display_key.singularize() + '!'
		}
		else {
			return this.parent_object[this.key]
		}
	}

	set value(new_value) {
		// create a BlindValue object with new_value, or if it already exists, update the obj w/ new_value
		this.parent_object[this.key] = new_value
	}

	get classes() {
		let classes = ['blind']
		if( this.mode === 'append' ) classes.push('blind-append')
		for( let class_name in this.blinds.blind_class_conditions ){
			let value = this.blinds.blind_class_conditions[class_name]
			if( is.function(value) ){
				let bool_func = value
				if( bool_func(this.blinds.object, this.display_key, this.key) ) classes.push(class_name)
			}
			else if( is.boolean(value) ){
				let bool = value
				if( bool ) classes.push(class_name)
			}
		}
		return classes
	}

	get htmlified() {
		return	'<div id="' + this.id + '" class="' + this.classes_htmlified + '">'
					+ '<div class="key" data-key="'+this.key+'">'
						+ this.display_key_htmlified + '&nbsp&nbsp'
					+ '</div>'
					+ '<div class="value mousetrap" ' + this.contenteditable_htmlified + '>'
						+ this.value_htmlified
					+ '</div>'
					+ this.icon_htmlified
			+ '</div>'
	}

	get icon_htmlified() {
		if( this.mode === 'append' ) return '<img class="icon append" src="images/add.svg" />'
		return (this.blinds.edit_save_icon)? '<img class="icon edit-save" src="images/'+editOrSave(this.state)+'.svg" />': ''
		function editOrSave(state) {
			return (state === 'read')? 'edit': 'save'
		}
	}

	get display_key_htmlified() {
		return this.blinds.render(this.blinds.transform_key(this.display_key, this.blinds.object) + ':') // marked wraps this in paragraph tags and NEWLINES. NEWLINES are rendered in HTML as a single space
	}

	get value_htmlified() {
		let value_string = is.array(this.value)? this.value.join(', '): this.value
		if(this.state === 'write'){
			if( this.mode === 'chosen' ) return as_select_html(this.value)
			else return value_string
		}
		else if(this.state === 'read') {
			return this.blinds.render(value_string)
		}
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

//////////////////////////// BLINDVALUE CLASS ////////////////////////////
class BlindValue {

	constructor(value) {
		// if string, store it
		// if array, map el to [el, true] and store
	}

	get this() {
		return this.iterable.this
	}

	set _iterable(array) {
		// this could possibly be something other than an array if necessary
		// if an iterable already exists, complain
		// the array can also hold a hidden 'this' key which holds the pointer to the blind value
		this.__iterable = array
	}

	get iterable() {
		return this.__iterable
	}

	select(el) {
		// if element exists, make sure its true
		// otherwise, create it true
	}

	deselect(el) {
		// if el exists, make false
		// otherwise, create it false
	}

	_append(el, bool) {
		// create it w/ bool value
	}

	_delete(el) {
		// we may need this in the future
	}
}

////////////////////////////// HELPERS //////////////////////////////
function as_select_html(array_selected) {
	let client_node_names = graph.nodeNamesList()

	let string = '<select class="tags" multiple>'
	_.each(client_node_names, function(el){
		string = string + '<option value="'+el+'" '+selected(array_selected, el)+'>'+el+'</option>'
	})
	string = string + '</select>'
	return string
}

function selected(array_selected, el){
	if( _.contains(array_selected, el) ) return 'selected' // we set property selected to true, so it's pre-selected
	return ''
}

////////////////////////////// EXPORTS //////////////////////////////
return Blinds

}) // end of define
