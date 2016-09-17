define( ["check-types"], function(is) {

// we want to grab magic values too!
window.hasOwnPropertyOrGetter = function(obj, key) {
	return obj.hasOwnProperty(key) || obj.__lookupGetter__(key) // see http://ejohn.org/blog/javascript-getters-and-setters/
}

// when pushing an array ref onto an array, use pushArray for proper flattenation:
window.pushArray = function(arr1, arr2) {
	arr1.push.apply(arr1, arr2)
}

// Array Remove - By John Resig (MIT Licensed) - Edited by Matt Lancellotti
window.remove = function(arr, from, to) {
	var rest = arr.slice((to || from) + 1 || arr.length)
	arr.length = from < 0 ? arr.length + from : from
	return pushArray(arr, rest)
}

// we might get away with monkey patching string things:
String.prototype.capitalizeFirstLetter = function() {
	return this.charAt(0).toUpperCase() + this.slice(1)
}
String.prototype.singularize = function() {
	if( this === 'dependencies' ) return 'dependency'
	if( this.charAt(this.length-1) === 's' ) return this.slice(0, this.length-1)
	else return this
}
// we are appending these to window in order to make them global variables
window.reduce_string = function(string) {
	if( !is.string(string) ) die('Expected type string.  Got type: ' + typeof string)
	return string.replace(/[_\W]/g, '').toLowerCase()
}
window.die = function(string) {
	alert(string)
	throw(string)
}
window.def = function(input) {
	// die("This function should return TRUE for empty arrays [].  verify that it does.  then see why blorg populated synonyms in all our nodes!.")
	return typeof(input) !== 'undefined'
}

window.log = function(thing) {
	console.log(thing)
}
window.logj = function(one, two) {
	if( def(two) ){
		log(one + JSON.stringify(two))
	}
	else{
		log(JSON.stringify(one))
	}
}

}) // end of define
