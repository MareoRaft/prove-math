define( ['jquery', 'underscore', 'check-types', 'profile'], function($, _, check, undefined) {


/////////////////////////////////// HELPERS ///////////////////////////////////

//////////////////////////////////// MAIN /////////////////////////////////////
var prefs = {
	"displayNameCapitalization": "title", // can be null, "sentence", or "title"
	"underlineDefinitions": false, // can be true or false // do you want definitions to be underlined in the DAG view?
	"showDescriptionOnHover": false, // can be true or false
}


return {
	prefs: prefs,
}


}); // end of define
