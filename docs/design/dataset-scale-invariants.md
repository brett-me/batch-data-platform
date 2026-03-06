
# Week 1 – Dataset Scale and Invariants

## Target Row Counts

The initial synthetic dataset should be intentionally modest in scale so that it remains easy to inspect, debug, and rerun while still behaving like a realistic small production system.

Planned starting scale:

- **Customers:** 100
- **Plans:** 3
- **Subscriptions:** approximately 120–150
- **Invoices:** several hundred
- **Payments:** several hundred

This scale is large enough to support realistic joins, distributions, and later quality checks, while remaining small enough for manual inspection during early development.

## Target Date Window

The initial dataset should cover the **last 12 months**.

This provides enough time depth for recurring billing behaviour, multiple invoice cycles, later period-based rollups, and historical correctness checks, without making the seed process unnecessarily complex.

## Structural Relationship Rules

The dataset should obey the following core structural rules:

- Every subscription must reference a valid customer.
- Every subscription must reference a valid plan.
- Every invoice must reference a valid subscription.
- Every payment must reference a valid invoice.

These rules define the baseline integrity of the dataset and should remain true in the initial seeded state.

## Notes

The initial dataset should be **mostly clean** at baseline.

Imperfections such as duplicates, late-arriving records, unpaid invoices, or late payments should be introduced deliberately and in controlled amounts in later steps of the programme. This preserves a stable foundation for development and makes later reliability drills easier to reason about.

All raw tables should include:

- `ingest_batch_id`
- `ingested_at`

These fields provide ingestion metadata so that each row can later be traced back to a specific batch and load time.

Seed includes controlled unpaid invoices and late payments for later rollups

## Week 1 Seed Reset Semantics (Temporary)

During Week 1, the seed process uses a simple reset-and-reload approach for baseline development speed and predictability:

- `truncate` seeded tables
- reset identity counters
- reinsert deterministic rows

Truncation order must respect foreign key dependencies (truncate child tables before parent tables), or truncate related tables in a single statement.

This is a deliberate early-stage choice and will later be replaced by a rerun-safe idempotent strategy (e.g., upserts / conflict handling) as the platform reliability work progresses.