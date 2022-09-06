export PGDATABASE := lastfm_db
export PGUSER := alumnodb
export PGPASSWORD := alumnodb
export PGCLIENTENCODING := LATIN9
export PGHOST := localhost
export DJANGOPORT = 8001
export HEROKUHOST = quiet-anchorage-37484
# must update the value of HEROKUHOST
export HEROKUREPO := git:remote $(HEROKUHOST) # cambiar a nueva app
PSQL = psql
CMD = python3 manage.py
HEROKU = heroku run export SQLITE=1 &
# Add applications to APP variable as they are
# added to settings.py file
APP = recommender

server:
	$(CMD) runserver $(DJANGOPORT)

reset_db: clear_db update_db create_super_user

clear_db:
	@echo Clear Database
	dropdb --if-exists $(PGDATABASE)
	createdb

shell:
	@echo manage.py  shell
	@$(CMD) shell

dbshell:
	@echo manage.py dbshell
	@$(CMD) dbshell

populate:
	@echo populate database
	python3 ./manage.py populate

static:
	@echo manage.py collectstatic
	python3 ./manage.py collectstatic

update_db:
	$(CMD) makemigrations $(APP)
	$(CMD) migrate

create_super_user:
	$(CMD) shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); \
	 User.objects.filter(username='alumnodb').exists() or User.objects.create_superuser('alumnodb', 'admin@myproject.com', 'alumnodb')"

clear_update_db:
	@echo del migrations and make migrations and migrate
	rm -rf */migrations
	python3 ./manage.py makemigrations $(APP) 
	python3 ./manage.py migrate

test_catalog_coverage:
	coverage erase
	coverage run --omit="*/test*" --source=catalog ./manage.py test catalog.tests_models catalog.tests_additional
	coverage report -m -i

test_catalog_datamodel:
	$(CMD) test catalog.tests_models --keepdb

coverage:
	coverage erase
	coverage run --omit="*/test*" --source=catalog,orders ./manage.py test
	coverage report -m -i

# other commands that may be useful but require tuning
#test_heroku:
#	$(HEROKU) $(CMD) test datamodel.tests_models.GameModelTests --keepdb & wait
#	$(HEROKU) $(CMD) test datamodel.tests_models.MoveModelTests --keepdb & wait
#	$(HEROKU) $(CMD) test datamodel.tests_models.my_tests --keepdb & wait
#
#test_query:
#	python3 test_query.py
#
#test_query_heroku:
#	$(HEROKU) python3 test_query.py
#
#config_heroku:
#	heroku login
#	heroku $HEROKUREPO
#

# PRIMERO GIT INIT, LUEGO HEROKU DYNO:SCALE UP LUEGO ESTO
heroku_push:
	git push heroku master

heroku_bash:
	heroku run bash

heroku_dbshell:
	heroku pg:psql

heroku_branch_push:
	git push heroku bookshop:master

heroku_createsuperuser:
	heroku run $(CMD) shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('alumnodb', 'admin@myproject.com', 'alumnodb')"


# locally backup database
dump_db:
	pg_dump -h localhost -p 5432 -U alumnodb $(PGDATABASE) --no-owner --no-acl -f $(PGDATABASE).dump
# restore database in heroku
heroku_restore_db:
	heroku psql DATABASE_URL --app $(HEROKUHOST) < $(PGDATABASE).dump

connect_db:
	$(PSQL) -U alumnodb -d $(PGDATABASE)
