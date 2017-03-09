db.nodes.createIndex(
	{
		'_id': 'text',
		// old-style nodes
		'_name': 'text',
		'_number': 'text',
		'_negation': 'text',
		'_synonyms': 'text',
		'_plurals': 'text',
		'_description': 'text',
		// new-style nodes
		// I DON"T KNOW IF INCLUDING THINGS LIKE IMPORTANT (number) or EXAMPLES (array) will ruin the 'text' classification of this index.  for now, i simply omitt those.
		'attrs.name.value': 'text',
		'attrs.number.value': 'text', // NOT a number
		'attrs.description.value': 'text',
		'attrs.negation.value': 'text',
	},
	{
		weights: {
			'_id': 6,
			// old-style nodes
			'_name': 10,
			'_number': 8,
			'_negation': 8,
			'_synonyms': 8,
			'_plurals': 8,
			'_description': 6,
			// new-style nodes
			'attrs.name.value': 10,
			'attrs.number.value': 8,
			'attrs.description.value': 6,
			'attrs.negation.value': 8,
		},
		name: 'search'
	}
)
