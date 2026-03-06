.PHONY: help up down reset status psql ddl seed checks test

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
	docker compose up -d

down:
	docker compose down

reset:
	docker compose down -v
	docker compose up -d

status:
	docker compose ps

psql:
	psql -h localhost -p 5432 -U postgres -d postgres

ddl:
	psql -h localhost -p 5432 -U postgres -d postgres \
		-f sql/ddl/001_create_core_tables.sql \
		-f sql/ddl/002_create_subscriptions.sql

seed:
	@echo "seed target placeholder"

checks:
	@echo "checks target placeholder"

test:
	@echo "test target place holder"

