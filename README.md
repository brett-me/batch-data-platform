# Batch Data Platform

Batch-orientated data platform built with reliability, reproducibility and operational controls in mind.

## Purpose

This repository defines a local-first batch data platform with a synthetic SaaS billing domain used to exercise reproducible infrastructure, schema management, and controlled database operations.

The current implementation establishes the operational foundation of the platform: containerised local infrastructure, standardised Makefile commands, environment-based configuration, and initial schema definition in PostgreSQL.

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

### Run the full local flow

```bash
make up
make ddl
make seed
make checks
make psql
make down
```

## Repository Structure

```text
.
├── docker-compose.yml    # local infrastructure definition
├── Makefile              # operational interface (make targets)
├── .env.example          # configuration template
├── docs/                 # design and architecture documentation
├── sql/ddl/              # schema definition files
├── sql/checks/           # data quality checks
├── scripts/              # operational scripts
└── src/                  # Python package
```

## Current State

The repository includes:

- a containerised PostgreSQL instance defined in `docker-compose.yml`
- a local configuration contract using `.env.example`
- Makefile targets for platform start-up, shutdown, database access, schema application, seeding, and checks
- schema DDL files in `sql/ddl/` for customers, plans, subscriptions, invoices, and payments
- a deterministic seeding script in `scripts/seed.py` that loads a synthetic billing dataset (including controlled unpaid invoices and late payments)
- sanity checks in `sql/checks/001_sanity.sql`
- domain documentation in `docs/week1-domain-model.md`

This establishes a reproducible local database environment, a repeatable schema + seed workflow, and basic validation primitives for later reliability drills.

## Clean-room Rebuild

To wipe and rebuild the local platform:

```bash
make reset
make ddl
make seed
make checks
```

This removes the local database volume and recreates the platform from scratch.

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
