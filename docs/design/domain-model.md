# Week 1 – Raw Domain Model

## Context

This repository implements a synthetic SaaS billing domain to exercise data platform design, reproducibility, and reliability practices.

The raw schema defines the core business entities, their grain, and their relationships prior to SQL implementation.

---

## Customers

**Grain**  
One row per customer account in the SaaS system.

**Type**  
State (identity table).

**Description**  
Represents an account registered in the platform. A customer may have zero or many subscriptions over time.

**Relationships**
- Referenced by `subscriptions`.

---

## Plans

**Grain**  
One row per plan definition in the product catalogue.

**Type**  
State / reference.

**Description**  
Represents the set of offerings (e.g. Basic, Pro). Plans may change over time. Subscriptions reference the plan definition at the time of enrolment. Each subscription stores the agreed price at enrolment to preserve historical correctness.

**Relationships**
- Referenced by `subscriptions`.

---

## Subscriptions

**Grain**  
One row per customer–plan time period.

**Type**  
Time-bound state (lifecycle table).

**Description**  
Represents a customer’s enrolment in a specific plan for a defined period of time. A customer may have multiple subscriptions over time (e.g. upgrades, cancellations, reactivations).

Each subscription stores the agreed price at the time of enrolment to preserve historical pricing accuracy.

**Relationships**
- References `customers` (`customer_id`).
- References `plans` (`plan_id`).
- Referenced by `invoices`.

---

## Invoices

**Grain**  
One row per invoice (billing event).

**Type**  
Event.

**Description**  
Represents an issued billing record for a subscription for a specific billing period. The invoice captures the amount due as an immutable value and must not derive pricing dynamically from current plan definitions.

**Relationships**
- References `subscriptions` (`subscription_id`).
- Referenced by `payments`.

---

## Payments

**Grain**  
One row per payment attempt or transaction.

**Type**  
Event.

**Description**  
Represents a payment event against an invoice. Payments are append-only. Retries and failures are recorded as separate rows to preserve full historical accuracy.

**Relationships**
- References `invoices` (`invoice_id`).

## Raw Table Ingestion Metadata

All raw tables in the initial schema should include the following ingestion metadata columns:

- `ingest_batch_id`
- `ingested_at`

These fields exist in addition to the business columns for each entity.

`ingest_batch_id` identifies the batch or load that inserted the row.  
`ingested_at` records the timestamp at which the row entered the platform.

This ensures that raw data can later be traced back to a specific ingestion event and supports rerun safety, debugging, and reliability drills.