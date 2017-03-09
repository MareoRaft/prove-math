db.nodes.createIndex(
	{
		'_id': 'text',
		'_name': 'text',
		'_synonyms': 'text',
		'_plurals': 'text',
		'_description': 'text',
	},
	{
		weights: {
			'_name': 10,
			'_synonyms': 8,
			'_plurals': 8,
			'_negation': 8,
			'_id': 6,
			'_description': 6,
		},
		name: 'search'
	}
)
