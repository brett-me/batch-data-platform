# Batch Data Platform

Batch-orientated data platform built with reliability, reproducibility and operational controls in mind.

## Purpose

This repository defines a local-first batch data platform with a synthetic SaaS billing domain and a focus on reproducible infrastructure, schema management, and controlled database operations.

The current implementation establishes the operational foundation of the platform: containerised local infrastructure, standardised Makefile commands, environment-based configuration, deterministic seeding, and schema definition in PostgreSQL.

The platform is designed to be built incrementally while maintaining a professional, production-minded repository structure.

## Quickstart

Create a local environment configuration:

```bash
cp .env.example .env
```

Start the local platform:

```bash
make up
```

Run a smoke check:

```bash
make smoke
```

Apply the current database schema:

```bash
make ddl
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

Stop the platform when finished:

```bash
make down
```

### Discover available Commands

To see the current operational interface for the platform:

```bash
make help
```

### Run the full local flow

```bash
make up
make smoke
make ddl
make seed
make checks
make down
```

## Repository Structure

```text
.
├── docker-compose.yml    # local infrastructure definition
├── Makefile              # operational interface (make targets)
├── .env.example          # configuration template
├── docs/
│   ├── decisions/        # architectural and operational decision records
│   ├── design/           # design notes and modelling artefacts
│   └── runbooks/         # operational runbooks
├── sql/
│   ├── ddl/              # schema definition files
│   └── checks/           # data quality checks
├── scripts/              # operational scripts
└── src/                  # Python package
```

## Current State

The repository includes:

- a containerised PostgreSQL instance defined in `docker-compose.yml`
- a local configuration contract using `.env.example`
- Makefile targets for platform start-up, shutdown, smoke checks, database access, schema application, seeding, and checks
- schema DDL files in `sql/ddl/` for customers, plans, subscriptions, invoices, and payments
- a deterministic seeding script in `scripts/seed.py` that loads a synthetic billing dataset, including controlled unpaid invoices and late payments
- a smoke check in `scripts/smoke.py`
- sanity checks in `sql/checks/001_sanity.sql`
- design documentation in `docs/design/`, including the domain model and dataset scale/invariant notes
- a formal rerun-semantics decision record in `docs/decisions/0001-seed-rerun-semantics.md`

This establishes a reproducible local database environment, a repeatable schema and seed workflow, and basic validation primitives for later reliability drills.

## Clean-room Rebuild

Use this sequence to wipe local state and rebuild the platform from scratch:

1. Reset the local platform:

```bash
make reset
```

2. Run a smoke check:

```bash
make smoke
```

3. Apply the schema:

```bash
make ddl
```

4. Seed synthetic data:

```bash
make seed
```

5. Run sanity checks:

```bash
make checks
```

A successful clean-room rebuild means the platform can be recreated from a known clean state using only the repository's documented interface.

## Configuration

Create a local environment file from the example:

```bash
cp .env.example .env
```

Environment variables define database connection settings and runtime parameters for local development.

Typical variables include:

- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `SEED`
- `SCALE`
