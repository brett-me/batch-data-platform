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
	python3 -m pip install -e ".[test]"

# platform lifecycle
up:
	docker compose up -d

status:
	docker compose ps

smoke:
	set -a; . ./.env; set +a; python3 scripts/smoke.py

down:
	docker compose down

reset:
	docker compose down -v
	docker compose up -d

# database / data workflow
ddl:
	set -a; . ./.env; set +a; psql -v ON_ERROR_STOP=1 -h "$$DB_HOST" -p "$$DB_PORT" -U "$$DB_USER" -d "$$DB_NAME" \
		-f sql/ddl/001_create_core_tables.sql \
		-f sql/ddl/002_create_subscriptions.sql \
		-f sql/ddl/003_create_invoices.sql \
		-f sql/ddl/004_create_payments.sql

seed:
	set -a; . ./.env; set +a; python3 scripts/seed.py

checks:
	set -a; . ./.env; set +a; psql -v ON_ERROR_STOP=1 -h "$$DB_HOST" -p "$$DB_PORT" -U "$$DB_USER" -d "$$DB_NAME" \
		-f sql/checks/001_sanity.sql

psql:
	set -a; . ./.env; set +a; psql -h "$$DB_HOST" -p "$$DB_PORT" -U "$$DB_USER" -d "$$DB_NAME"


# code quality
test:
	pytest

lint:
	ruff check src scripts tests

