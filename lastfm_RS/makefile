export PGDATABASE := lastfm_db
export PGUSER := alumnodb
export PGPASSWORD := alumnodb
export PGCLIENTENCODING := UTF8
export PGHOST := localhost
export DJANGOPORT = 8001

PSQL = psql
CMD = python3 manage.py
APP = recommender

server:
	$(CMD) runserver $(DJANGOPORT)

reset_db: clear_db update_db create_super_user

clear_db:
	@echo Clear Database
	dropdb --if-exists $(PGDATABASE)
	createdb -E utf8

shell:
	@echo manage.py  shell
	@$(CMD) shell

dbshell:
	@echo manage.py dbshell
	@$(CMD) dbshell

static:
	@echo manage.py collectstatic
	python3 ./manage.py collectstatic

update_db:
	$(CMD) makemigrations $(APP)
	$(CMD) migrate

create_super_user:
	$(CMD) shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); \
	 User.objects.filter(username='$(PGUSER)').exists() or User.objects.create_superuser('$(PGUSER)', 'admin@myproject.com', '$(PGUSER)')"

clear_update_db:
	@echo del migrations and make migrations and migrate
	rm -rf */migrations
	python3 ./manage.py makemigrations $(APP)
	python3 ./manage.py migrate

# locally backup database
dump_db:
	pg_dump -h localhost -p 5432 -U $(PGUSER) $(PGDATABASE) --no-owner --no-acl -f $(PGDATABASE).dump

# restore from backup
restore_db:
	make clear_db
	unzip $(PGDATABASE).zip
	$(PSQL) -U $(PGUSER) $(PGDATABASE) < $(PGDATABASE).dump
	rm $(PGDATABASE).dump

connect_db:
	$(PSQL) -U $(PGUSER) -d $(PGDATABASE)
