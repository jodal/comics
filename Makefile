MANAGE = PYTHONPATH=. comics/manage.py

.PHONY: all clean reload shell test coverage

all: clean reload

clean:
	find . -iname \*.pyc -delete

reload:
	find apache -iname \*.wsgi -exec touch {} \;

shell:
	$(MANAGE) shell --settings=comics.settings.dev

test:
	$(MANAGE) test --settings=comics.settings.test

coverage:
	$(MANAGE) test --settings=comics.settings.coverage
