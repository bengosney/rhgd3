.PHONY := install, install-dev, help, init, pre-init, postgres, postgres-down, test
.DEFAULT_GOAL := install-dev

INS=$(wildcard requirements.*.in)
REQS=$(subst in,txt,$(INS))
HOOKS=$(.git/hooks/pre-commit)

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

init: pre-init install-dev $(HOOKS) postgres ## Initalise a dev enviroment
	@echo "Read to dev"

postgres-down:
	@echo "Stopping any excisting postgres containers"
	@docker stop stl-postgres || true
	@docker rm stl-postgres || true

postgres: postgres-down
	docker run --rm --name rhgd-postgres -p 5432:5432 -e POSTGRES_PASSWORD=cJYuVv3uaBeP78Le -e POSTGRES_USER=rhgdesign -d postgres

test:
	pytest --cov=. .
