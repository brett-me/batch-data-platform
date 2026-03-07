SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c

ENV_RUN = set -a; . ./.env; set +a;

.PHONY: help dev-install up status smoke down reset ddl seed checks psql test lint

# discovery
help:
	@echo "Targets:"
	@echo "  help         - show available commands"
	@echo "  dev-install  - install Python development dependencies"
	@echo "  up           - start local platform"
	@echo "  status       - check container status"
	@echo "  smoke        - verify database reachability and expected tables"
	@echo "  down         - stop local platform"
	@echo "  reset        - wipe and rebuild platform"
	@echo "  ddl          - apply schema files in order"
	@echo "  seed         - load deterministic synthetic data"
	@echo "  checks       - run sanity checks"
	@echo "  psql         - open database shell"
	@echo "  test         - run unit tests"
	@echo "  lint         - run Python lint checks"

# environment / setup
dev-install:
	@echo "==> Installing Python development dependencies"
	python3 -m pip install -e ".[test]"

# platform lifecycle
up:
	@echo "==> Starting local platform"
	docker compose up -d

status:
	@echo "==> Checking container status"
	docker compose ps

smoke:
	@echo "==> Running smoke check"
	$(ENV_RUN) python3 scripts/smoke.py

down:
	@echo "==> Stopping local platform"
	docker compose down

reset:
	@echo "==> Resetting local platform"
	docker compose down -v
	docker compose up -d

# database / data workflow
ddl:
	@echo "==> Applying schema"
	$(ENV_RUN) psql -v ON_ERROR_STOP=1 -h "$$DB_HOST" -p "$$DB_PORT" -U "$$DB_USER" -d "$$DB_NAME" \
		-f sql/ddl/001_create_core_tables.sql \
		-f sql/ddl/002_create_subscriptions.sql \
		-f sql/ddl/003_create_invoices.sql \
		-f sql/ddl/004_create_payments.sql

seed:
	@echo "==> Seeding synthetic data"
	$(ENV_RUN) python3 scripts/seed.py

checks:
	@echo "==> Running sanity checks"
	$(ENV_RUN) psql -v ON_ERROR_STOP=1 -h "$$DB_HOST" -p "$$DB_PORT" -U "$$DB_USER" -d "$$DB_NAME" \
		-f sql/checks/001_sanity.sql

psql:
	@echo "==> Opening database shell"
	$(ENV_RUN) psql -h "$$DB_HOST" -p "$$DB_PORT" -U "$$DB_USER" -d "$$DB_NAME"


# code quality
test:
	@echo "==> Running unit tests"
	pytest

lint:
	@echo "==> Running Python lint checks"
	ruff check src scripts tests

