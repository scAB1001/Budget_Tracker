For form stuff (drop downs etc)
https://wtforms.readthedocs.io/en/2.3.x/validators/

Each time our models change, we will run flask db migrate and then flask db upgrade.
https://flask-sqlalchemy.palletsprojects.com/en/2.x/
https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/#querying-records
https://docs.sqlalchemy.org/en/14/orm/query.html



### After db changes:
$ flask db migrate
Migrations>versions> 'latest version file, find:

1. batch_op.create_foreign_key(None, 'landlord', ['landlord_id'], ['id'])
2. batch_op.drop_constraint(None, type_='foreignkey')
Change the None to 'fk_landlord_id'.

then finish with $ flask db upgrade...


# ***If you run $ flask fb upgrade by accident and see the name constraint err. 
Add in the changes above to 'fk_landlord_id'. Then type:

$ flask db stamp head
$ flask db upgrade

This will make it the latest version file, and upgrade for the table. 
However the foreign key constraint is still not in the database.

$ flask db migrate
Add the 'fk_landlord_id' changes to the latest (stamped) migration version.

then finish with $ flask db upgrade.
