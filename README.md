# Batch Data Platform

[![CI](https://github.com/brett-me/batch-data-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/brett-me/batch-data-platform/actions/workflows/ci.yml)

Local-first PostgreSQL batch data platform for reproducible schema application, deterministic synthetic data generation, and operational validation.

## Purpose

This repository provides a local-first batch data platform built around a synthetic SaaS billing domain.

It supports reproducible schema application, deterministic synthetic data generation, and operational validation through a documented command-line workflow.

The current implementation is intended for local rebuild, inspection, and validation of a small PostgreSQL-backed batch platform.

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

Depending on local PostgreSQL credential setup, psql may prompt for a password.

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
make ddl
make smoke
make seed
make checks
make down
```

## Configuration

Create a local environment file from the example:

```bash
cp .env.example .env
```

Environment variables define database connection settings and seed controls for local development

Key variables include:

- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`  
  PostgreSQL connection settings used by Make targets and Python scripts.

- `SEED`  
  Controls deterministic synthetic data generation. The same seed should produce the same logical dataset.

- `SCALE`  
  Controls the size of the seeded dataset. The default value is intended for fast local iteration.

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

`make reset` recreates the local database container and removes the local PostgreSQL volume. This deletes the current local database state.

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

## Before You Push

Run the basic local quality gates before pushing changes:

```bash
make test
make lint
```

If the change affects schema, seeded data, or validation logic, also run:

```bash
make checks
```

## Repository Structure

```text
.
├── .github/
│   └── workflows/        # CI workflow definitions
├── Makefile              # operational interface
├── README.md             # repository overview and operating instructions
├── docker-compose.yml    # local infrastructure definition
├── docs/
│   ├── decisions/        # architectural and operational decisions
│   │   └── 0001-seed-rerun-semantics.md
│   ├── design/           # domain and data-model design notes
│   │   ├── dataset-scale-invariants.md
│   │   └── domain-model.md
│   └── runbooks/         # operational validation and troubleshooting notes
│       └── rebuild-validation.md
├── pyproject.toml        # Python project metadata and development dependencies
├── scripts/              # CLI entry-point scripts
│   ├── seed.py
│   └── smoke.py
├── sql/
│   ├── checks/           # sanity and validation queries
│   │   └── 001_sanity.sql
│   └── ddl/              # schema definition files
│       ├── 001_create_core_tables.sql
│       ├── 002_create_subscriptions.sql
│       ├── 003_create_invoices.sql
│       └── 004_create_payments.sql
├── src/
│   └── batch_data_platform/  # reusable Python package code
│       ├── __init__.py
│       ├── config.py
│       ├── seeding.py
│       └── smoke_checks.py
└── tests/                # unit tests
    └── test_smoke_unit.py
```

## Current State

The repository currently provides:

- a local PostgreSQL-backed batch platform defined with Docker Compose
- a Makefile-based operational interface for setup, rebuild, schema application, seeding, validation, testing, and linting
- schema definition files for customers, plans, subscriptions, invoices, and payments
- deterministic synthetic data generation for local development and validation
- smoke checks and sanity checks for platform and data validation
- reusable Python package code under `src/batch_data_platform/`
- CLI entry-point scripts for seeding and smoke validation
- unit tests and CI workflow checks for basic code and workflow verification
- supporting design notes, decision records, and runbook documentation under `docs/`

The current implementation supports local rebuild, schema application, seeded data generation, and validation through a documented command-line workflow.
