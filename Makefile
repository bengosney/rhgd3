.PHONY := install, install-dev, help, init, pre-init, postgres, postgres-down, test
.DEFAULT_GOAL := install-dev

INS=$(wildcard requirements.*.in)
REQS=$(subst in,txt,$(INS))
HOOKS=$(.git/hooks/pre-commit)
PGC_NAME=rhgd-postgres
PG_PASSWORD=cJYuVv3uaBeP78Le
PG_USERNAME=rhgdesign
PG_DATABASE=rhgdesign
HEROKU_APP=still-caverns-78460
DUMP_DIR=dumps

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

requirements.%.txt: requirements.%.in
	@echo "Builing $@"
	@pip-compile -q -o $@ $^

requirements.txt: requirements.in
	@echo "Builing $@"
	@pip-compile -q $^

install: requirements.txt ## Install production requirements
	@echo "Installing $^"
	@pip-sync $^

install-dev: requirements.txt $(REQS) ## Install development requirements (default)
	@echo "Installing $^"
	@pip-sync $^

$(HOOKS):
	pre-commit install

pre-init:
	pip install wheel pip-tools

init: pre-init install-dev $(HOOKS) postgres-import ## Initalise a dev enviroment
	@echo "Read to dev"

postgres-down:
	@echo "Stopping any excisting postgres containers"
	@docker stop $(PGC_NAME) || true
	@docker rm $(PGC_NAME) || true

$(DUMP_DIR):
	mkdir -p $@
	chown -R $(shell whoami) $@

postgres: $(DUMP_DIR)
	docker container inspect $(PGC_NAME) 2>&1 > /dev/null || docker run --rm --name $(PGC_NAME) -v $(shell pwd)/$(DUMP_DIR):/dumps -p 5432:5432 -e POSTGRES_PASSWORD=$(PG_PASSWORD) -e POSTGRES_USER=$(PG_USERNAME) -d postgres

postgres-import: postgres $(DUMP_DIR)
	docker exec -it $(PGC_NAME) pg_restore --verbose --clean --no-acl --no-owner -h localhost -U $(PG_USERNAME) -d $(PG_DATABASE) /dumps/$(shell ls dumps | head -n 1)

dump: $(DUMP_DIR)
	@cd $(DUMP_DIR) && \
	echo "Creating backup" && \
	heroku pg:backups:capture --app still-caverns-78460 && \
	echo "Downloading backup" && \
	heroku pg:backups:download --app still-caverns-78460


test:
	pytest --cov=. .
