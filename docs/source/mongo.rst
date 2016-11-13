MongoDB Setup
=====================


Installing MongoDB
------------------------
Well, you can try ``brew``!  If you are using Linux, we suggest using Mongo's source file with ``apt-get`` instead of the default.



Creating a Search Index
-------------------------------
In MongoDB, once you are in your database of choice, ``show collections`` will list `system.indexes` among your other collections.  This may not be helpful, but it's proof that indexes exist!

For the rest of this example, I will assume you are working with the `nodes` collection.  The commands ``db.nodes.getIndexes()`` (or ``db.nodes.getIndices()``) will list any indices associated with the collection.  You will always see the default index listed, which looks something like this::

	{
		"v": 1,
		"key": {
			"_id": 1
		},
		"name": "_id_",
		"ns": "provemath.nodes"
	}

To create our custom node search index, use the command::

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

We still haven't pinned down exactly which weights we'd like to use.

Run ``db.nodes.getIndexes()`` again to see your new index.

Note that there can only be ONE custom index per collection.

If you messed up or need to delete an index, type::

	db.nodes.dropIndex(name)

where `name` is the name of the index that you see in the output of ``db.nodes.getIndexes()``.

You can also check out `this resource <https://dzone.com/articles/mongodb-full-text-search>`_ for more help.


