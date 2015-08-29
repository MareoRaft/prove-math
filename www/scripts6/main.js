require.config({
	// by eliminating baseUrl, everything becomes relative, which is the convention that KaTeX files follow.
	// in order for this to work, we CANT USE PATHS SHORTCUTS FOR directories either
	// now i'm trying KaTeX by CDN instead.
	baseUrl: "scripts/lib", // the default base is the directory of the INDEX.HTML file
	paths: { // other paths we want to access
		jquery: "http://code.jquery.com/jquery-1.11.2.min", // and the .js is added like always by require
		underscore: "https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.2/underscore-min",
		// backbone: "https://cdnjs.cloudflare.com/ajax/libs/backbone.js/1.1.2/backbone-min",
		// d3: "https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min",
		d3: "d3-for-development",
		katex: "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.3.0/katex.min", // or 0.2.0
		mathjax: "http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML&amp;delayStartupUntil=configured",
	},
	shim: { // allows us to bind variables to global (with exports) and show dependencies without using define()
		underscore: { exports: "_" },
		// backbone: { deps: ["jquery", "underscore"], exports: "Backbone" },
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
	"d3-and-svg",
	"browser-detect",
	"check-types",
	"katex",
	"mathjax",
	"profile",
], function(
	$,
	_,
	d3AndSVG,
	browser,
	check,
	katex,
	mathjax,
	undefined
){

// websocket stuff!
//var ws = ('WebSocket' in window)? new WebSocket("ws://provemath.org/websocket"): undefined; // url to send websocket messages
var ws = ('WebSocket' in window)? new WebSocket("ws://localhost/websocket"): undefined;
if( !def(ws) ){
	die('Your browser does not support websockets, which are essential for this program.')
}

ws.onopen = function(){
	ws.send("Hello, world, Remember to clear cache if needed!")
}
ws.onmessage = function(event){
	var unbundled = JSON.parse(event.data)
	var graph = unbundled
	// for( var i=0; i < graph.nodes.length; i++){
	// 	alert(graph.nodes[i])
	// }
	d3AndSVG.processNewGraph(graph)
}


$('#test').click(hello)
$('#AddProof').click(add_proof)
$('#Submit').click(send_node_info)




// setup all the things we can do before actually getting the data:
function hello(){
	var letsTry = JSON.stringify({"contents":"I want to send this over upon a click in a json file preferably"})
    //var contents = $('#cool').val()
    ws.send("For my sanity")
}

function add_proof(){
    var proof_type=document.getElementById("ProofType");
    var selectedValue = proof_type.options[proof_type.selectedIndex].value;
    var proofs = $('#Proofs').val();
    // To Fix so not to repeat if statement for comma
    if(document.getElementById('inputList').innerHTML!==""){
		$('#inputList').append(",");
    }

    $('#inputList').append(JSON.stringify({"type":selectedValue, "content":proofs}));
}

function send_node_info(){
	try{
	    //To Fix
	    var name = $('#Name').val()
	    var plural = $('#Plural').val()
	    var content = $('#Content').val()
	    var examples = $('#Examples').val()
	    var counterexamples = $('#Counterexamples').val()
	    var intuition = $('#Intuition').val()
	    var notes = $('#Notes').val()
	    var importance = document.getElementById('Importance').value

	    var radios = document.getElementsByName('type');
	    var type = check_radio_button(radios).value;
	    var proofs = "["+document.getElementById('inputList').innerHTML+"]";

	    ws.send(importance)
	    if(type === "Theorem"){
		    var clean_proofs = JSON.parse(proofs)
		}
	    else{
	    	var clean_proofs = JSON.parse("{}")
		}
	    ws.send(type)
	    ws.send(JSON.stringify({
	    	"name": name,
	    	"plural": plural,
	    	"content": content,
	    	"type": type,
	    	"proofs": clean_proofs,
			"importance": importance,
	    	"examples": examples,
	    	"counterexamples": counterexamples,
	    	"intuition": intuition,
	    	"notes": notes,
		}))
	  }
	catch(err){
		alert("There is an error")
	}
}

function check_radio_button(radios){
	for(var i=0; i < radios.length; i++){
	    var current = radios[i]
	    if(current.checked){
			return current
	    }
	}
	alert("Please choose a type!")
}



/////////////////////////////////// MATHJAX ///////////////////////////////////
$(".math").each(function(){ // this is set up as client-side rendering.  see #usage above and use katex.renderToString for server side.
	var texText = $(this).text();
	var el = $(this).get(0);
	var addDisplay = "";
	if(el.tagName === "DIV"){
		addDisplay = "\\displaystyle";
	}
	try{
		katex.render(addDisplay+texText, el);
	}
	catch(err) {
		if (err.__proto__ === katex.ParseError.prototype) {
			$(this).html('$'+texText+'$')
		} else {
			$(this).html("<span class='err'>"+'Hi! '+err+"</span>");
		}
	}
})


//////////////////////////// TEST D3 FUNCTIONALITY ////////////////////////////
// 1. Add three nodes and three links.
setTimeout(function() {
	var new_graph = {
		"nodes": [
			{_id: "at", _importance: 1, _type: 'exercise', _name: 'pigeonhole principal'},
			{_id: "b", _importance: 8, _type: "theorem", _name: 'pigeonhole theorem'},
			{_id: "c", _importance: 5, _type: "definition", _name: 'Bernoulli number'},
		],
		"links": [
			{source: "at", target: "b"}, {source: "at", target: "c"}, {source: "b", target: "c"},
		],
	}
	d3AndSVG.processNewGraph(new_graph)
}, 0);

// 2. Remove node B and associated links.
setTimeout(function() {
	// remove b
	// remove a-b
	// remove b-c
	var new_graph = {
		"nodes": [
			{_id: "b", remove: true},
		],
	}
	d3AndSVG.processNewGraph(new_graph)
}, 3000);

// // Add node B back.
setTimeout(function() {
	var graph = {
		nodes: [
			{_id: "b", _importance: 4, _type: "definition", _name: 'sequence'},
		],
		links: [
			{source: "at", target: "b"}, {source: "b", target: "c"},
		],
	}
	d3AndSVG.processNewGraph(graph)
}, 6000);







}); // end require
