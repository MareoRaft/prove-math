db.nodes.dropIndex("search");
db.nodes.createIndex(
	{
		'_id': 'text',
		// new-style nodes
		// I DON"T KNOW IF INCLUDING THINGS LIKE IMPORTANT (number) or EXAMPLES (array) will ruin the 'text' classification of this index.  for now, i simply omitt those.
		// 'attrs.name.value': 'text',
		'attrs.number.value': 'text', // NOT a number
		'attrs.description.value': 'text',
		'attrs.negation.value': 'text',
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
			'_id': 10,
			// new-style nodes
			'attrs.name.value': 17,
			'attrs.number.value': 39,
			'attrs.description.value': 5,
			'attrs.negation.value': 7,
			// old-style nodes
			'_name': 17,
			'_number': 39,
			'_negation': 7,
			'_synonyms': 7,
			'_plurals': 7,
			'_description': 5
		},
		name: 'search'
	}
);
