//////////////////////////// BLINDS ////////////////////////////
function blindsTest(obj) {
	blinds.init({
		window_id: 'node-template-blinds',
		blind_class: 'node-attribute',
		render: marked,
		expand_array: true
	});

	// blinds.open({
	// 	object: obj,
	// })

	// blinds.open({
	// 	object: obj,
	// 	separate_array_keys: ['one', 'threekey', 'notinobj'],
	// })

	// blinds.open({
	// 	object: obj,
	// 	separate_array_keys: ['one', 'threekey', 'notinobj'],
	// 	keys: ['one', 'two'],
	// })

	blinds.open({
		object: obj,
		keys: ['_name', '_description', '_synonyms', '_plurals', 'notes', 'intuitions', 'examples', 'counterexamples', 'dependencies'],
		collapse_array_keys: ['dependencies', 'synonyms', 'plurals']
	});
}