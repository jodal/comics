.PHONY: all clean reload shell test coverage

all: clean reload

clean:
	find comics/ -iname \*.pyc -delete

reload:
	find apache/ -iname \*.wsgi -exec touch {} \;

shell:
	comics/manage.py shell --settings=comics.settings.dev

test:
	comics/manage.py test --settings=comics.settings.testing

coverage:
	comics/manage.py test --settings=comics.settings.coverage
