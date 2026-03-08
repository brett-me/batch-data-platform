# Batch Data Platform

[![CI](https://github.com/brett-me/batch-data-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/brett-me/batch-data-platform/actions/workflows/ci.yml)

Batch-oriented data platform built with reliability, reproducibility and operational controls in mind.

## Purpose

This repository defines a local-first batch data platform with a synthetic SaaS billing domain and a focus on reproducible infrastructure, schema management, and controlled database operations.

The current implementation establishes the operational foundation of the platform: containerised local infrastructure, standardised Makefile commands, environment-based configuration, deterministic seeding, and schema definition in PostgreSQL.

The platform is developed incrementally while maintaining a professional, production-minded repository structure.

## Quickstart

Create a local environment configuration:

```bash
cp .env.example .env
```

Install Python development dependencies:

```bash
make dev-install
```

Start the local platform:

```bash
make up
```

Apply the current database schema:

```bash
make ddl
```

Run a smoke check:

```bash
make smoke
```

Seed synthetic data:

```bash
make seed
```

Run sanity checks:

```bash
make checks
```

Open a database shell:

```bash
make psql
```

You will be prompted for the Postgres password (default: `postgres`).

Stop the platform:

```bash
make down
```

### Useful operational commands

Show the available Make targets:

```bash
make help
```

Check container status:

```bash
make status
```

### Run the full local flow

```bash
make dev-install
make up
make status
make smoke
make ddl
make seed
make checks
make down
```

## Before You Push

Run the basic local quality gates before pushing changes:

```bash
make test
make lint
make checks
```

## Repository Structure

```text
.
├── docker-compose.yml    # local infrastructure definition
├── Makefile              # operational interface (make targets)
├── .env.example          # configuration template
├── .github/
│   └── workflows/        # CI workflow definitions
├── docs/
│   ├── decisions/        # architectural and operational decision records
│   ├── design/           # design notes and modelling artefacts
│   └── runbooks/         # operational runbooks
├── sql/
│   ├── ddl/              # schema definition files
│   └── checks/           # data quality checks
├── scripts/              # CLI entry-point scripts
├── src/
│   └── batch_data_platform/  # reusable Python package code
└── tests/                # unit tests
```

## Current State

The repository includes:

- a containerised PostgreSQL instance defined in `docker-compose.yml`
- a local configuration contract using `.env.example`
- Makefile targets for environment setup, platform lifecycle, smoke checks, database access, schema application, seeding, validation, testing, and linting
- schema DDL files in `sql/ddl/` for customers, plans, subscriptions, invoices, and payments
- reusable Python package code in `src/batch_data_platform/`
- CLI entry-point scripts in `scripts/seed.py` and `scripts/smoke.py`
- a deterministic seeding workflow that loads a synthetic billing dataset with controlled unpaid invoices and late payments
- a smoke check in `scripts/smoke.py`
- sanity checks in `sql/checks/001_sanity.sql`
- unit tests in `tests/test_smoke_unit.py`
- a CI workflow in `.github/workflows/ci.yml`
- design documentation in `docs/design/`
- a formal rerun-semantics decision record in `docs/decisions/0001-seed-rerun-semantics.md`

This establishes a reproducible local database environment, a repeatable schema and seed workflow, basic validation primitives, and an initial automated testing layer.

## Clean-room Rebuild

Use this sequence to wipe local state and rebuild the platform from scratch:

1. Reset the local platform:

```bash
make reset
```

2. Apply the schema:

```bash
make ddl
```

3. Run a smoke check:

```bash
make smoke
```

4. Seed synthetic data:

```bash
make seed
```

5. Run sanity checks:

```bash
make checks
```

## Troubleshooting

### `make up` succeeds but the platform is not ready

Check container state first:

```bash
make status
```

If the PostgreSQL container is still starting, wait a few seconds and run the command again.

### `make smoke` fails because expected tables are missing

The smoke check validates both:

- database reachability
- existence of the expected tables

Apply the schema before running the smoke check:

```bash
make ddl
make smoke
```

### `make psql`, `make ddl`, or `make checks` prompts for a password

Database connection settings are loaded from `.env`.

For local development convenience, configure a PostgreSQL password file at:

```text
~/.pgpass
```

Example entry for the default local setup:

```text
localhost:5432:postgres:postgres:postgres
```

Then lock file permissions:

```bash
chmod 600 ~/.pgpass
```

### Port `5432` is already in use

Check whether another PostgreSQL instance or container is already bound to port `5432`.

Stop the local platform first:

```bash
make down
```

If the conflict is outside this repository, stop the other local service or change the configured port.

### Local database state appears inconsistent

Reset the local platform and rebuild from a clean state:

```bash
make reset
make ddl
make smoke
make seed
make checks
```

`make reset` removes the local PostgreSQL volume and starts the container again. This deletes the current local database state. 

`make reset` recreates the local database container but does not apply schema. Until `make ddl` runs, `make smoke` will fail because the expected tables do not yet exist.

### `make checks` fails

Run the local workflow in order:

```bash
make ddl
make smoke
make seed
make checks
```

If checks still fail, inspect the output first. The sanity checks are designed to fail loudly when required conditions are not met.

### Need a quick view of available commands

Show the current Make targets:

```bash
make help
```

## Configuration

Create a local environment file from the example:

```bash
cp .env.example .env
```

Environment variables define database connection settings and runtime parameters for local development.

Key variables include:

- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`  
  PostgreSQL connection settings used by Make targets and Python scripts.

- `SEED`  
  Controls deterministic synthetic data generation. The same seed should produce the same logical dataset.

- `SCALE`  
  Controls the size of the seeded dataset. The default value is intended for fast local iteration.
