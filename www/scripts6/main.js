define( [
	"jquery",
	"underscore",
	"browser-detect",
	"check-types",
	"katex",
	"mathjax",
	"profile",
	"marked",
	"graph",
	"node",
	"graph-animation",
	"blinds",
	"chosen",
	"user",
], function(
	$,
	_,
	browser,
	is,
	katex,
	mathjax,
	undefined,
	marked,
	graph,
	Node,
	graphAnimation,
	blinds,
	chosen,
	user
){


////////////////////////////// GLOBALS ///////////////////////////////
let css_show_hide_array = ['#avatar', '#login-circle', '#logout-circle']


/////////////////////////// INITIALIZATION ///////////////////////////
let user_dict = JSON.parse($('body').attr('data-user-dict-json-string'))
log('user dict is...')
logj(user_dict)
if( is.emptyObject(user_dict) ){
	// not logged in:
	loginInit()
	show('#login')
}
else{
	// logged in:
		// $("#display_name").html(user_dict["id_name"]) // add this back in when we have a drop down
		$("#avatar").attr("src", user_dict["profile_pic"])
		hide('#login-circle')
	show('#overlay')
}
user.init(user_dict) // this should ALSO be triggered by jQuery when they login

graphAnimation.init({
	// window_id: 'graph-containter', // had to use 'body' // after animation actually works, put init inside $(document).ready() to guarantee that container was loaded first.  if that DOES NOT WORK, then respond to http://stackoverflow.com/questions/13865606/append-svg-canvas-to-element-other-than-body-using-d3 with that issue
	node_label: node => { if(node.type !== 'exercise') return node.gA_display_name }, // exercise names should NOT appear
	node_radius: node => 7.9 * Math.sqrt(node.importance), // 7.5
	circle_class_conditions: {
		'bright-circle': node => node.learned,
		'axiom-circle': node => node.type === 'axiom' || node.type === null,
		'definition-circle': node => node.type === 'definition',
		'theorem-circle': node => node.type === 'theorem',
		'exercise-circle': node => node.type === 'exercise',
	},
	circle_events: { // this will not update if the user changes their preferences.  maybe we can hand graph-animation the user, and then it can access the prefs itself
		mouseover: node => { if( user.prefs.show_description_on_hover ) node.gA_display_name = node.description },
		mouseout: node => { if( user.prefs.show_description_on_hover ) node.gA_display_name = node.display_name },
	},
})
show('svg') // both svg and node-template are hidden on load
show('#banner')


function katexRenderIfPossible(string) {
	let content = string.substr(1, -1)
	try{
		content = katex.renderToString(content) // katex.render takes in element as second parameter
	}
	catch(error) {
		if (error.__proto__ === katex.ParseError.prototype) {
			alert('error1')
			return string // the original string unchanged (for mathjax to snatch up later)
		} else {
			alert('error2')
			return "<span class='err' style='color:red;'>"+'ERROR: '+error+"</span>"
		}
	}
	alert(content)
	return content
}

blinds.init({
	window_id: 'node-template-blinds',
	keys: ['name', 'description', 'synonyms', 'plurals', 'notes', 'intuitions', 'examples', 'counterexamples', 'proofs', 'dependencies'],
	collapse_array_keys: ['dependencies', 'synonyms', 'plurals'],
	append_keys: ['name', 'description', 'synonyms', 'plurals', 'notes', 'intuitions', 'examples', 'counterexamples', 'proofs', 'dependencies'],
	render: function(string) {
		// run katex
		// string = string.replace(/\$[^\$]*\$/g, katexRenderIfPossible)
		// return string
		// make all \ into \\ instead, so that they will be \ again when marked is done. This is for MathJax postrender compatability.
		string = string.replace(/\\/g, '\\\\')
		return marked(string)
	},
	post_render: function() {
		// the following should be equivalent to // mathjax.Hub.Queue(['Typeset', mathjax.Hub])
		mathjax.Hub.Typeset() // this can't be passed in without the parenthesis
	},
	transform_key: keyToDisplayKey,
	expand_array: true,
	blind_class_conditions: {
		'node-attribute': true,
		animated: user.prefs.animate_blinds,
		flipInX: user.prefs.animate_blinds,
		empty: (node, display_key, key) => is.null(node[key]) || (is.array(node[key]) && (is.emptyArray(node[key]) || is.emptyString(node[key][0]))),
	},
	chosen: true,
})
let current_node = {}
$('#toggle-learn-state').click(function(){
	current_node.learned = !current_node.learned
	updateNodeTemplateLearnedState()
	graphAnimation.update()
})
function updateNodeTemplateLearnedState(){
	if( current_node.learned ){
		$('#toggle-learn-state').html('<img src="images/light-on.png">learned!')
	}else{
		$('#toggle-learn-state').html('<img src="images/light-off.png">not learned')
	}
}

let host = $('body').attr('data-host')
let ws = ('WebSocket' in window)? new WebSocket("ws://"+host+"/websocket"): undefined;
if( !def(ws) ) die('Your browser does not support websockets, which are essential for this program.')

ws.jsend = function(raw_object) {
	$.extend(raw_object, {identifier: user.get_identifier(), client_node_ids: graph.nodeIdsList()})
	ws.send(JSON.stringify(raw_object))
}
ws.onopen = function() {
	ws.jsend({command: 'open'})
}
ws.onmessage = function(event) { // i don't think this is hoisted since its a variable definition. i want this below graphAnimation.init() to make sure that's initialized first
	let ball = JSON.parse(event.data)
	if( ball.command === 'populate-oauth-urls' ) {
		oauth_url_dict = ball.url_dict
	}
	else if( ball.command === 'load-user' ) {
		user.init(ball.user_dict)
		hide('#login')
		show('#overlay')
	}
	else if( ball.command === 'load-graph' ) {
		let raw_graph = ball.new_graph
		_.each(raw_graph.nodes, function(raw_node, index) { // raw_node here is just a temp copy it seems
			raw_graph.nodes[index] = new Node(raw_node); // so NOW it is a REAL node, no longer raw //
		})
		let ready_graph = raw_graph
		graph.addNodesAndLinks({
			nodes: ready_graph.nodes,
			links: ready_graph.links,
		})
	}
	else if( ball.command === 'remove-edges' ) {
		graph.removeLinks({
			node_id: ball.node_id,
			dependency_ids: ball.dependency_ids,
		})
	}
	else if( ball.command === 'display-error' ) {
		alert('error: '+ball.message)
	}
        else if(ball.command === 'search-results'){
	    alert('Search results: '+JSON.stringify(ball.results))
	}

	else die('Unrecognized command '+ball.command+'.')
}

$(document).on('jsend', function(Event) {
	ws.jsend(Event.message)
})
$(document).on('add-links', function(Event) {
	graph.addNodesAndLinks({
		links: Event.message,
	})
})
$(document).on('request-node', function(Event) {
	ws.jsend({command: 'request-node', node_id: Event.message})
})
$(document).on('save-node', function(){
	ws.jsend({ command: 'save-node', node_dict: current_node.dict() })
})


////////////////////////// LOGIN/LOGOUT STUFF //////////////////////////
var oauth_url_dict = undefined

$('#x').click(function() {
	hide('#login')
		hide('#avatar')
		hide('#logout-circle')
		show('#login-circle')
	show('#overlay')
})
$('#login-circle').click(function() {
	hide('#overlay')
	show('#login')
})
$('#login-button').click(login)
$('#password, #username').keypress(function(event) { if(event.which === 13 /* Enter */) {
	login()
}})
$('.image-wrapper').click(function() {
	$('.image-wrapper').removeClass('invalid')
})
$('#account-type, #username, #password').keyup(function() { // keyup to INCLUDE whatever was just typed in .val()
	if($(this).val() !== '') {
		$(this).removeClass('invalid')
	}
})
$('#logout-circle').click(logout)


function login() {
	if( !def(oauth_url_dict) ) alert('oauth login broken.')
	let account_type = $('input[type=radio][name=provider]:checked').val()
	if( !def(account_type) || account_type === '' ){
		if( !def(account_type) ){
			$('.image-wrapper').addClass('invalid')
		}
		if( account_type === '' ){
			$('#social-icon-container > img').addClass('invalid')
		}
	} else {
		location.href = oauth_url_dict[account_type]
	}
}
function logout(){
	delete_cookie()
	hide('#overlay')
	show('#login')
}


///////////////////////////// SEARCH BAR /////////////////////////////
$('#search-box').keypress(function(event) { if(event.which === 13 /* Enter */) {
	ws.jsend({ command: 'search', search_term: $('#search-box').val() })
}})


//////////////////////////// ACTION STUFF ////////////////////////////
$('#add-node').click(function(){
	graph.addNode(new Node())
})


//////////////////////////// TOGGLE STUFF ////////////////////////////
$(document).on('node-click', function(Event){
	current_node = graph.nodes[Event.message] // graph.nodes is a DICTIONARY of nodes
	updateNodeTemplateLearnedState()
	blinds.open({
		object: current_node,
	})
	hide('svg')
	hide('#overlay')
	show('#node-template')
	if( false /*mode !== 'learn'*/){
		ws.jsend({ command: "re-center-graph", central_node_id: current_node.id })
	}
})

$('#back').click(fromBlindsToGraphAnimation)
$(document).keyup(function(event) { if(event.which === 27 /* Esc */) { // right now this runs even if the blinds are NOT the frontmost thing, which could lead to unpredictable behavior
	fromBlindsToGraphAnimation()
}})
function fromBlindsToGraphAnimation(){
	if( user.prefs.animate_blinds ){
		$('.node-attribute').addClass('animated flipOutX')
		$('.node-attribute').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', toggleToGraphAnimation)
	}
	else toggleToGraphAnimation()
}
function toggleToGraphAnimation() {
	hide('#node-template')
	show('svg')
	show('#overlay')
	blinds.close()
}

////////////////////////////// HELPERS //////////////////////////////
function hide(css_selector) {
	let $selected = $(css_selector)
	if( !_.contains(css_show_hide_array, css_selector) ){
		$selected.css('height', '0')
		$selected.css('width', '0')
		$selected.css('overflow', 'hidden')
	}else{
		// $selected.addClass('hidden')
		$selected.css('visibility', 'hidden')
	}
}
function show(css_selector) { // this stuff fails for svg when using .addClass, so we can just leave show and hide stuff in the JS.
	let $selected = $(css_selector)
	if( !_.contains(css_show_hide_array, css_selector) ){
		$selected.css('height', '100%')
		$selected.css('width', '100%')
		$selected.css('overflow', 'scroll')
	}else{
		// $selected.removeClass('hidden')
		$selected.css('visibility', 'visible')
	}
}

function keyToDisplayKey(word, node) {
	if( word === 'description' ) return node.type
	if( word === 'dependencies' || word === 'synonyms' || word === 'plurals' ) return word // we want these to stay plural
	if( word[word.length - 1] === 's' ) return word.substr(0, word.length - 1)
	return word // word may have ALREADY been singular
}

function loginInit() {
	$('#account-type').chosen({
		allow_single_deselect: true,
		inherit_select_classes: true,
		search_contains: true,
		width: '100%'
	}).change(function(){
		$('.account-type .chosen-single').removeClass('invalid')
	})
}

function delete_cookie() {
	document.cookie = 'mycookie=; expires=Thu, 01 Jan 1970 00:00:01 GMT;'
}

}) // end define
