# Dataset Scale and Invariants

## Purpose

This document defines the expected scale, temporal coverage, structural invariants, and seed behaviour assumptions for the initial synthetic dataset.

These constraints keep the dataset easy to inspect and rerun while still supporting realistic batch platform development, validation, and downstream modelling.

---

## Target Dataset Scale

The initial dataset is intentionally modest in scale so that it remains easy to inspect, debug, and rerun during early platform development.

Expected baseline scale:

- **Customers:** 100
- **Plans:** 3
- **Subscriptions:** approximately 120-150
- **Invoices:** several hundred
- **Payments:** several hundred

This scale is large enough to support realistic joins, distributions, and quality checks, while remaining small enough for manual inspection and deterministic local testing.

---

## Target Date Window

The initial dataset should cover the **most recent 12 months**.

This provides sufficient time depth for recurring billing behaviour, multiple invoice cycles, period-based rollups, and historical correctness checks without making the seed process unnecessarily complex.

---

## Structural Invariants

The seeded dataset must satisfy the following baseline referential rules:

- Every subscription references a valid customer.
- Every subscription references a valid plan.
- Every invoice references a valid subscription.
- Every payment references a valid invoice.

These invariants define the minimum structural integrity expected of the baseline dataset.

---

## Baseline Data Behaviour

The initial seeded dataset should be **mostly clean by design**.

Data imperfections such as duplicate records, late-arriving records, and other reliability edge cases should be introduced deliberately and in controlled amounts in later stages of the programme. This preserves a stable baseline for development and makes later reliability exercises easier to reason about.

The baseline seed may include controlled cases such as unpaid invoices and late payments where these support downstream modelling and validation scenarios.

---

## Raw-Layer Ingestion Metadata

All raw tables include the following ingestion metadata in addition to their business columns:

- `ingest_batch_id`
- `ingested_at`

These fields support ingestion traceability by identifying the batch that inserted each row and the timestamp at which the row entered the platform.

---

## Seed Reset Semantics

During the initial platform stage, the seed process uses a reset-and-reload approach to prioritise development speed, predictability, and deterministic reruns:

- truncate seeded tables
- reset identity counters
- reinsert deterministic rows

Reset behaviour must respect foreign-key dependencies, either by truncating child tables before parent tables or by truncating related tables in a dependency-safe statement.

This is an intentional early-stage platform choice and may later be replaced by a rerun-safe idempotent loading strategy, such as conflict handling or upsert-based loads, as the platform evolves.