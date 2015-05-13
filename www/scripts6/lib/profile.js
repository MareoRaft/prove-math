define( [], function() {

// return {
// 	die: function(string) {
// 		alert(string);
// 		throw(string);
// 	},
// 	def: function(input) {
// 		return typeof(input) !== 'undefined';
// 	},
// }

window.die = function(string) {
	alert(string);
	throw(string);
}
window.def = function(input) {
	return typeof(input) !== 'undefined';
}

}); // end of define
