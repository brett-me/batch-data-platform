.PHONY: help up down reset psql ddl seed checks test

help:
	@echo "Targets:"
	@echo "  up     - start local platform"
	@echo "  down   - stop local platform"
	@echo "  reset  - wipe + rebuild platform"
	@echo "  psql   - open DB shell"
	@echo "  ddl    - apply schema"
	@echo "  seed   - seed data"
	@echo "  checks - run sanity checks"
	@echo "  test   - run unit tests"

up:
	@echo "up target placeholder"

down:
	@echo "down target placeholder"

reset:
	@echo "rest target placeholder"

psql:
	psql -h localhost -p 5432 -U postgres -d postgres

ddl:
	@echo "ddl target placeholder"

seed:
	@echo "seed target placeholder"

checks:
	@echo "checks target placeholder"

test:
	@echo "test target place holder"

