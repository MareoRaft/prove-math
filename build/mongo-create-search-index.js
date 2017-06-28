db.nodes.dropIndex("search");
db.nodes.createIndex(
	{
		'_id': 'text',
		// new-style nodes
		// I DON"T KNOW IF INCLUDING THINGS LIKE IMPORTANT (number) or EXAMPLES (array) will ruin the 'text' classification of this index.  for now, i simply omit those.
		'attrs.name.value': 'text',
		'attrs.number.value': 'text', // NOT a number
		'attrs.examples.value': 'text', // an ARRAY of strings.  Mongo DOES support this!
		'attrs.counterexamples': 'text',
		'attrs.description.value': 'text',
		'attrs.intuitions.value': 'text',
		'attrs.notes.value': 'text',
		'attrs.dependencies.value': 'text',
		'attrs.plurals.value': 'text',
		'attrs.negation.value': 'text',
		'attrs.proofs.value': 'text',
		// old-style nodes
		'_name': 'text',
		'_number': 'text',
		'_negation': 'text',
		'_synonyms': 'text',
		'_plurals': 'text',
		'_description': 'text'
	},
	{
		weights: {
			// old and new style nodes
			'_id': 20,
			// new-style nodes
			'attrs.name.value': 42,
			'attrs.number.value': 78,
			'attrs.examples.value': 4,
			'attrs.counterexamples': 3,
			'attrs.description.value': 10,
			'attrs.intuitions.value': 6,
			'attrs.notes.value': 4,
			'attrs.dependencies.value': 3,
			'attrs.plurals.value': 15,
			'attrs.negation.value': 15,
			'attrs.proofs.value': 3,
			// old-style nodes
			'_name': 42,
			'_number': 78,
			'_negation': 15,
			'_synonyms': 15,
			'_plurals': 15,
			'_description': 10
		},
		name: 'search'
	}
);
