MongoDB
=====================


Installing MongoDB
------------------------
Well, you can try ``brew``!  If you are using Linux, we suggest using Mongo's source file with ``apt-get`` instead of the default.



Creating a Search Index
-------------------------------
This NO LONGER needs to be done manually, as we have a build process in `gulpfile.js` and a file `build/mongo-create-search-index.js` that does it automatically when running the gulp build.  But I will LEAVE THE LEGACY EXPLANATION BELOW ANYWAY.

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



Running MongoDB
------------------
First, the mongo daemon (`mongod`) needs to be running.  If things were configured nicely (which they are NOT), then::

	sudo service mongod start

would work, but you should do it manually with::

	sudo /usr/local/bin/mongod --logpath /var/db/mongodb/mongod.log --logappend --config /usr/local/etc/mongodb.conf --dbpath /var/db/mongodb

Now that the mongo daemon is running, you can access the mongo shell via::

	mongo



Backing up provemath db on MongoDB
-----------------------------------
Make sure you have the correct bind IP configured in ``build/mongod.conf`` (If you're not sure, then it's probably 127.0.0.1).  You can read more about MongoDB config options in the `mongo docs config <https://docs.mongodb.com/manual/reference/configuration-options/#configuration-file>`_.

We already have a build process called `dump` in ``gulpfile.js`` that does the backup for you.  Just run::

    gulp dump

and the provemath db in MongDB will be backed up to the folder ``server/data/mongo-dumps/server-blackberry.2018-03-03T15:55:07+00:00`` with the appropriate date and time at the end.

You can create a copy of this backup to a safe location::

    scp -r freebsd@provemath.org:prove-math/server/data/mongo-dumps/server-blackberry.2018-03-03T15:55:07+00:00 .



Restoring provemath db to MongoDB
-----------------------------------
To restore, use the `mongorestore` command (more at `mongo docs mongorestore <https://docs.mongodb.com/manual/reference/program/mongorestore/>`_)::

    mongorestore prove-math/server/data/mongo-dumps/server-blackberry.2018-03-03T15:55:07+00:00


