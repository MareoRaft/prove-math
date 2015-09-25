define( ['underscore', 'check-types', 'profile', 'user', 'marked'],
function( _,            check,         undefined, user,   marked) {


////////////////////////////////// HELPERS ////////////////////////////////////
function hide(css_selector){
	$(css_selector).css('overflow', 'hidden') // we can move this to SCSS file too
	$(css_selector).css('border-width', '0') // we may not need this
	$(css_selector).css('height', '0')
}

function show(css_selector){
	// restore any borders if there were any (not relevant now)
	$(css_selector).css('height', $(window).height())
	$(css_selector).css('width', $(window).width())
	$(css_selector).css('overflow', 'scroll')
}

//////////////////////////////// NODE FRONTEND ////////////////////////////////
var colorClass1Keys = ['name', 'description', 'synonyms', 'plurals', 'notes', 'intuitions']
var colorClass2Keys = ['examples', 'counterexamples']
var colorClass3Keys = ['dependencies']
function getColorClass(node, key) {
	var string = ''
	if( node.type === 'definition'){
		string = 'definition'
		if(_.contains(colorClass1Keys, key)){ // need to make an array to remove redunacny
			string = string + '-group-1'
		}
		else if(_.contains(colorClass2Keys, key)){
			string = string + '-group-2'
		}
		else if(_.contains(colorClass3Keys, key)){
			string = string + '-group-3'
		}
		else die('Unexpected key found: "' + key + '".')
	}
	else die('We can only color definitions so far.')
	return string
}

function keyToDisplayKey(node, word) { // used for allColorClassKeys
	if( word === 'description' ) return node.type
	if( word === 'dependencies' ) return 'dependencies' // we want this one to stay plural
	if( word[word.length - 1] === 's' ) return word.substr(0, word.length - 1)
	return word // word may have ALREADY been singular
}

function populateNodeAttribute(attr) {
	if( !check.array(attr.value) ) die('Value was not an array.  We are making them ALL arrays now.')
	if( attr.key === 'dependencies' ) attr.value = [attr.value.join(", ")]
	_.each(attr.value, function(value, index){
		if( !def(currentNode[attr.key][index.toString()+'-'+'state']) ){
			currentNode[attr.key][index.toString()+'-'+'state'] = 'read'
		}
		$('#node-template > section').append(
			'<div class="node-attribute ' + attr.colorClass + '">'
				+ '<span class="key" data-name="' + attr.key + '" data-index="' + index + '">'
					+ marked(keyToDisplayKey(attr.node, attr.key) + ':')
				+'</span>'
				+ ' ' // this space is not actually necessary, as marked wraps the above in paragraph tags and NEWLINES. NEWLINES are rendered in HTML as a single space
				+ '<span class="content">' + marked(value) + '</span>'
			+ '</div>'
		)
	})
}

var allColorClassKeys = colorClass1Keys.concat(colorClass2Keys).concat(colorClass3Keys)
var currentNode
function populateNodeTemplate(node) {
	currentNode = node
	_.each(allColorClassKeys, function(key){ // NO FOR OF LOOPS BC BABEL DIDNT MAKE IT WORK CONSISTENTLY
		if( node.hasOwnProperty(key) ){
			var value = node[key]
			if( value === '' ) die('Found an empty string')
			if( value === [] ) die('Found an empty array')
			populateNodeAttribute({node: node, key: key, value: value, colorClass: getColorClass(node, key)})
		}
	})
	$('.node-attribute').dblclick(function(){
		var $key = $(this).children('.key:first')
		var $content = $(this).children('.content:first')
		var state = currentNode[$key.attr('data-name')][$key.attr('data-index').toString() + '-state']
		if( state === 'read' ){
			startEditMode($(this), $key, $content)
			currentNode[$key.attr('data-name')][$key.attr('data-index').toString() + '-state'] = 'write'
		}
		else if( state === 'write' ){
			endEditMode($(this), $key, $content)
			currentNode[$key.attr('data-name')][$key.attr('data-index').toString() + '-state'] = 'read'
		}
		else die('Unexpected state "' + state + '".')
	})
	$('#learn').click(function(){
		currentNode.learned = true
	})
	$('#unlearn').click(function(){
		currentNode.learned = false
	})
}

function startEditMode(jQueryNodeAttributeObj, $key, $content) {
		// alert(JSON.stringify($key))
	var pureMarkdown = currentNode[$key.attr('data-name')][$key.attr('data-index')]
		// alert(pureMarkdown)
		// alert(check.string(pureMarkdown))
	$content.html(pureMarkdown)
	$content.prop('contenteditable', true)

	// set the cursor to the beginning and make it appear
	$content.focus() // <-- needed for Firefox
	var range = document.createRange()
	var sel = window.getSelection()
	range.setStart($content.get(0).childNodes[0], 0); // line 0, character 0
	range.collapse(true)
	sel.removeAllRanges()
	sel.addRange(range)
}

function endEditMode(jQueryNodeAttributeObj, $key, $content) {
	$content.prop('contenteditable', false)
	// take content, STORE IT, then display the marked() version of it
	if( check.array.of.string(currentNode[$key.attr('data-name')]) ){
		currentNode[$key.attr('data-name')][$key.attr('data-index')] = $content.html()
	}
	else die('Unexpected value of node stuff ' + currentNode[$key.attr('data-name')])

	$content.html(marked(currentNode[$key.attr('data-name')][$key.attr('data-index')]))
}



function unpopulateNodeTemplate() {
	$('#node-template > section').html('')
}

//////////////////////////////////// MAIN /////////////////////////////////////
return {
	hide: hide,
	show: show,
	populateNodeTemplate: populateNodeTemplate,
	unpopulateNodeTemplate: unpopulateNodeTemplate,
}


}); // end of define
