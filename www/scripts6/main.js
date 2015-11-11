require.config({
	// by eliminating baseUrl, everything becomes relative, which is the convention that KaTeX files follow.
	// in order for this to work, we CANT USE PATHS SHORTCUTS FOR directories either
	// now i'm trying KaTeX by CDN instead.
	baseUrl: "scripts/lib", // the default base is the directory of the INDEX.HTML file
	paths: { // other paths we want to access
		jquery: "http://code.jquery.com/jquery-1.11.2.min",
		underscore: "https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.2/underscore-min",
		d3: "d3-for-development", // if we add patches separately, then we can just use https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min
		katex: "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.3.0/katex.min", // or 0.2.0
		mathjax: "http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML&amp;delayStartupUntil=configured",
		// marked: "https://cdnjs.cloudflare.com/ajax/libs/marked/0.3.2/marked.min", // disabled for consistent development
		chosen: "https://cdnjs.cloudflare.com/ajax/libs/chosen/1.4.2/chosen.jquery.min",
		jsnetworkx: "https://raw.githubusercontent.com/fkling/JSNetworkX/v0.3.4/jsnetworkx", //actually we maybe should download this
	},
	shim: { // allows us to bind variables to global (with exports) and show dependencies without using define()
		underscore: { exports: "_" },
		chosen: { deps: ["jquery"] },
		mathjax: {
			exports: "MathJax",
			init: function (){
				MathJax.Hub.Config({
					tex2jax: {
						inlineMath: [['$','$'], ['\\(','\\)']],
						processEscapes: true, // this causes \$ to output as $ outside of latex (as well as \\ to \, and maybe more...)
					},
				});
				MathJax.Hub.Startup.onload();
				return MathJax;
			}
		},
	},
});

require( [
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
	check,
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

/////////////////////////// INITIALIZATION ///////////////////////////
let user_dict_json_string = $('body').attr('data-user-dict-json-string')
let user_dict = JSON.parse(user_dict_json_string)
if( check.emptyObject(user_dict) ){
	loginInit()
	show('#login')
}
user.init(user_dict) // this should ALSO be triggered by jQuery when they login

graphAnimation.init({
	// window_id: 'graph-containter', // had to use 'body' // after animation actually works, put init inside $(document).ready() to guarantee that container was loaded first.  if that DOES NOT WORK, then respond to http://stackoverflow.com/questions/13865606/append-svg-canvas-to-element-other-than-body-using-d3 with that issue
	node_label: node => { if(node.type !== 'exercise') return node.gA_display_name }, // exercise names should NOT appear
	node_radius: node => 7.9 * Math.sqrt(node.importance), // 7.5
	circle_class_conditions: {
		'bright-circle': node => node.learned,
		'axiom-circle': node => node.type === 'axiom',
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
	keys: ['name', 'description', 'synonyms', 'plurals', 'notes', 'intuitions', 'examples', 'counterexamples', 'dependencies'],
	collapse_array_keys: ['dependencies', 'synonyms', 'plurals'],
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
		'definition-group-1': (node, key) => _.contains(['name', 'description', 'synonyms', 'plurals', 'notes', 'intuitions'], key),
		'definition-group-2': (node, key) => _.contains(['examples', 'counterexamples'], key),
		'definition-group-3': (node, key) => _.contains(['dependencies'], key),
		animated: user.prefs.animate_blinds,
		flipInX: user.prefs.animate_blinds,
	},
	chosen: true,
})
let current_node = {}
$('#learn').click(function(){
	current_node.learned = true // does it grab current_node from outside scope? // YES
	graphAnimation.update()
})
$('#unlearn').click(function(){
	current_node.learned = false
	graphAnimation.update()
})

let host = $('body').attr('data-host')
let ws = ('WebSocket' in window)? new WebSocket("ws://"+host+"/websocket"): undefined;
if( !def(ws) ) die('Your browser does not support websockets, which are essential for this program.')

ws.jsend = function(raw_object) {
	ws.send(JSON.stringify(raw_object))
}
ws.onopen = function() {
}
ws.onmessage = function(event) { // i don't think this is hoisted since its a variable definition. i want this below graphAnimation.init() to make sure that's initialized first
	let ball = JSON.parse(event.data)
	if( ball.command === 'populate-oauth-urls' ) {
		oauth_url_dict = ball.url_dict
	}
	else if( ball.command === 'load-user' ) {
		user.init(ball.user_dict)
		hide('#login')
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
	else die('Unrecognized command '+ball.command+'.')
}

$(document).on('jsend', function(Event) {
	ws.jsend(Event.message)
})

///////////////////////////// LOGIN STUFF /////////////////////////////
var oauth_url_dict = undefined

$('#x').click(function(){
	hide('#login')
})
$('#login-button').click(login)
$('#password, #username').keypress(function(event) { if(event.which === 13) {
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

function login() {
	if( !def(oauth_url_dict) ) alert('oauth login broken.')
	// let account_type = $('#account-type').val()
	let account_type = $('input[type=radio][name=provider]:checked').val()
	// let username = $('#username').val()
	// let password = $('#password').val()
	// if any field is empty, complain
	// if( !def(account_type) || account_type === '' || username === '' || password === '' ){
	if( !def(account_type) || account_type === '' ){
		if( !def(account_type) ){
			$('.image-wrapper').addClass('invalid')
		}
		if( account_type === '' ){
			$('#social-icon-container > img').addClass('invalid')
		}
		// if( username === '' ){
		// 	$('#username').addClass('invalid')
		// }
		// if( password === '' ){
		// 	$('#password').addClass('invalid')
		// }
	} else {
		// ws.jsend({ command: 'login', account_type: account_type, username: username, password: password })
		// display SWoD?
		location.href = oauth_url_dict[account_type]
	}
}

//////////////////////////// TOGGLE STUFF ////////////////////////////
$(document).on('node-click', function(Event){
	current_node = graph.nodes[Event.message] // this assumed HASH of nodes
	blinds.open({
		object: current_node,
	})
	hide('#banner')
	hide('svg')
	show('#node-template')
})

$('#back').click(function(){
	if( user.prefs.animate_blinds ){
		$('.node-attribute').addClass('animated flipOutX')
		$('.node-attribute').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', toggleToGraphAnimation)
	}
	else toggleToGraphAnimation()
})

function toggleToGraphAnimation() {
	hide('#node-template')
	show('svg')
	show('#banner')
	blinds.close()
}

////////////////////////////// HELPERS //////////////////////////////
function hide(css_selector) {
	let $selected = $(css_selector)
	$selected.css('height', '0')
	$selected.css('width', '0')
	$selected.css('overflow', 'hidden')
}

function show(css_selector) { // this stuff fails for svg when using .addClass, so we can just leave show and hide stuff in the JS.
	let $selected = $(css_selector)
	$selected.css('height', '100%')
	$selected.css('width', '100%')
	$selected.css('overflow', 'scroll')
}

function keyToDisplayKey(word, node) {
	if( word === 'description' ) return node.type
	if( word === 'dependencies' ) return 'dependencies' // we want this one to stay plural
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

}); // end require
