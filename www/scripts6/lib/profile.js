define( [], function() {

// when pushing an array ref onto an array, use pushArray for proper flattenation:
Array.prototype.pushArray = function(arr) {
    this.push.apply(this, arr)
}

String.prototype.capitalizeFirstLetter = function() {
    return this.charAt(0).toUpperCase() + this.slice(1)
}

// we are appending these to window in order to make them global variables
window.die = function(string) {
	alert(string)
	throw(string)
}
window.def = function(input) {
	return typeof(input) !== 'undefined'
}

}) // end of define
