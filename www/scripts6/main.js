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
		// mathjax: {
		// 	exports: "MathJax",
		// 	init: function (){
		// 		MathJax.Hub.Config({
		// 			tex2jax: {
		// 				inlineMath: [['$','$'], ['\\(','\\)']],
		// 				processEscapes: true, // this causes \$ to output as $ outside of latex (as well as \\ to \, and maybe more...)
		// 			},
		// 		});
		// 		MathJax.Hub.Startup.onload();
		// 		return MathJax;
		// 	}
		// },
	},
});

require( [
	"jquery",
	"underscore",
	"browser-detect",
	"check-types",
	"katex",
	// "mathjax",
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
	// mathjax,
	undefined,
	marked,
	graph,
	Node,
	graphAnimation,
	blinds,
	chosen,
	user
){



//// test chosen
$('#cars').width("40%")
$('#cars').chosen()


/////////////////////////// INITIALIZATION ///////////////////////////
// alert(JSON.stringify(user.prefs))
user.init({ // this one should be triggered by jQuery when they login
	account_type: 'facebook',
	username: 'mischievous matt',
	password: 'jellybeans',
})
// alert(JSON.stringify(user.prefs))

let circle_events = {
	mouseover: node => { if( user.prefs.show_description_on_hover ) node.gA_display_name = node.description },
	mouseout: node => { if( user.prefs.show_description_on_hover ) node.gA_display_name = node.display_name },
}
circle_events[user.prefs.view_node_trigger] = node => $.event.trigger({ type: 'view-node', message: node.id })
graphAnimation.init({
	// window_id: 'graph-containter', // had to use 'body' // after animation actually works, put init inside $(document).ready() to guarantee that container was loaded first.  if that DOES NOT WORK, then respond to http://stackoverflow.com/questions/13865606/append-svg-canvas-to-element-other-than-body-using-d3 with that issue
	node_label: node => { if(node.type !== 'exercise') return node.gA_display_name }, // exercise names should NOT appear
	node_radius: node => 6 * Math.sqrt(node.importance),
	circle_class_conditions: {
		'bright-circle': node => node.learned,
		'definition-circle': node => node.type === 'definition',
		'theorem-circle': node => node.type === 'theorem',
		'exercise-circle': node => node.type === 'exercise',
	},
	circle_events: circle_events, // this will not update if the user changes their preferences.  maybe we can hand graph-animation the user, and then it can access the prefs itself
})
show('svg') // both svg and node-template are hidden on load

blinds.init({
	window_id: 'node-template-blinds',
	keys: ['name', 'description', 'synonyms', 'plurals', 'notes', 'intuitions', 'examples', 'counterexamples', 'dependencies'],
	collapse_array_keys: ['dependencies', 'synonyms', 'plurals'],
	render: marked,
	transform_key: keyToDisplayKey,
	expand_array: true,
	blind_class_conditions: {
		'node-attribute': true,
		'definition-group-1': (node, key) => _.contains(['name', 'description', 'synonyms', 'plurals', 'notes', 'intuitions'], key),
		'definition-group-2': (node, key) => _.contains(['examples', 'counterexamples'], key),
		'definition-group-3': (node, key) => _.contains(['dependencies'], key),
	},
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

// let ws = ('WebSocket' in window)? new WebSocket("ws://provemath.org/websocket"): undefined;
let ws = ('WebSocket' in window)? new WebSocket("ws://localhost/websocket"): undefined;
if( !def(ws) ) die('Your browser does not support websockets, which are essential for this program.')

ws.onopen = function() {
	ws.send("Hello, world, Remember to clear cache if needed!")
	// on the SERVER SIDE, on ws.onopen, before sending graph, send user info.
}
ws.onmessage = function(event) { // i don't think this is hoisted since its a variable definition. i want this below graphAnimation.init() to make sure that's initialized first
	let unbundled = JSON.parse(event.data)
	// here we can do 'command' logic to process various commands from server
	// 'load' command can direct to user.load()
	let raw_graph = unbundled
	_.each(raw_graph.nodes, function(raw_node, index) { // raw_node here is just a temp copy it seems
		raw_graph.nodes[index] = new Node(raw_node); // so NOW it is a REAL node, no longer raw
	})
	let ready_graph = raw_graph
	graph.addNodesAndLinks({
		nodes: ready_graph.nodes,
		links: ready_graph.links,
	})
}


//////////////////////////// TOGGLE STUFF ////////////////////////////
$(document).on('view-node', function(Event){
	current_node = graph.nodes[Event.message] // this assumed HASH of nodes
	blinds.open({
		object: current_node,
	})
	hide('svg')
	show('#node-template')
})

$('#back').click(function(){
	hide('#node-template')
	show('svg')
	blinds.close()
})


////////////////////////////// HELPERS //////////////////////////////
function hide(css_selector) {
	let $selected = $(css_selector)
	$selected.css('overflow', 'hidden') // we can move this to SCSS file too
	$selected.css('border-width', '0') // we may not need this
	$selected.css('height', '0')
}

function show(css_selector) {
	let $selected = $(css_selector)
	// restore any borders if there were any (not relevant now)
	$selected.css('height', $(window).height())
	$selected.css('width', $(window).width())
	$selected.css('overflow', 'scroll')
}

function keyToDisplayKey(word, node) {
	if( word === 'description' ) return node.type
	if( word === 'dependencies' ) return 'dependencies' // we want this one to stay plural
	if( word[word.length - 1] === 's' ) return word.substr(0, word.length - 1)
	return word // word may have ALREADY been singular
}


}); // end require
