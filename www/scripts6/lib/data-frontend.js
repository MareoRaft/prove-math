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
var colorClass1Keys = ['name', 'definition', 'theorem', 'synonyms', 'plurals', 'notes', 'intuitions']
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

function pluralToSingular(word) { // used for allColorClassKeys
	if( word === 'dependencies' ) return 'dependencies' // we want this one to stay plural
	if( word[word.length - 1] === 's' ) return word.substr(0, word.length - 1)
	return word // word may have ALREADY been singular
}

function populateNodeAttribute(attr) {
	if( check.string(attr.content) ) attr.content = [attr.content]
	if( attr.type === 'dependencies' ) attr.content = [attr.content.join(", ")]
	attr.type = pluralToSingular(attr.type)
	_.each(attr.content, function(content){
		$('#node-template > section').append(
			'<div class="node-attribute ' + attr.colorClass + '">'
			+ marked(attr.type + ': ' + content) + '</div>'
		)
	})
}

var allColorClassKeys = colorClass1Keys.concat(colorClass2Keys).concat(colorClass3Keys)
function populateNodeTemplate(node) {
	for( var key of allColorClassKeys ){
		if( node.hasOwnProperty(key) ){
			var content = node[key] // in the if statement below, make sure the content is not blank eithers or empty array
			populateNodeAttribute({type: key, content: content, colorClass: getColorClass(node, key)})
		}
		else if( _.contains(['definition', 'theorem', 'exercise'], key) && node.type === key ){
			var content = node.description
			populateNodeAttribute({type: key, content: content, colorClass: getColorClass(node, key)})
		}
	}
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
