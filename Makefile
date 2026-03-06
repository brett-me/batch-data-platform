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
	psql -v ON_ERROR_STOP=1 -h localhost -p 5432 -U postgres -d postgres \
		-f sql/ddl/001_create_core_tables.sql \
		-f sql/ddl/002_create_subscriptions.sql \
		-f sql/ddl/003_create_invoices.sql \
		-f sql/ddl/004_create_payments.sql

seed:
	python3 scripts/seed.py

checks:
	psql -h localhost -p 5432 -U postgres -d postgres \
		-f sql/checks/001_sanity.sql

test:
	@echo "test target place holder"

