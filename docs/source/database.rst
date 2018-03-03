Backing up and Restoring the Database
======================================



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


