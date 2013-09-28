run:
	reddoid/manage.py runserver --settings=reddoid.settings.local

syncdb:
	reddoid/manage.py syncdb --settings=reddoid.settings.local

test:
	reddoid/manage.py shell --settings=reddoid.settings.local

test:
	reddoid/manage.py test $TEST_APP --settings=reddoid.settings.local
