# Raw Domain Model

## Purpose

This repository models a synthetic SaaS billing domain to exercise batch data platform design, reproducibility, and reliability practices.

This document defines the raw domain entities, their intended grain, and their relationships before downstream transformation.

---

## Customers

**Grain**  
One row per customer account.

**Entity Type**  
State / identity.

**Description**  
Represents a customer account registered in the platform. A customer may hold zero or many subscriptions over time.

**Relationships**  
- Referenced by `subscriptions`.

---

## Plans

**Grain**  
One row per plan definition.

**Entity Type**  
State / reference.

**Description**  
Represents a product offering, such as Basic or Pro. Plan definitions may evolve over time. Subscriptions capture the agreed price at enrolment so that historical billing does not depend on the current plan definition.

**Relationships**  
- Referenced by `subscriptions`.

---

## Subscriptions

**Grain**  
One row per customer-plan subscription period.

**Entity Type**  
Time-bound state / lifecycle.

**Description**  
Represents a customer’s enrolment in a specific plan for a bounded period. A customer may have multiple subscriptions over time due to upgrades, cancellations, or reactivations.

Each subscription stores the agreed price at enrolment to preserve historical pricing correctness.

**Relationships**  
- References `customers` via `customer_id`.
- References `plans` via `plan_id`.
- Referenced by `invoices`.

---

## Invoices

**Grain**  
One row per invoice.

**Entity Type**  
Event.

**Description**  
Represents a billing event for a subscription and billing period. The invoice amount is recorded as an immutable value and must not be derived dynamically from the current plan definition.

**Relationships**  
- References `subscriptions` via `subscription_id`.
- Referenced by `payments`.

---

## Payments

**Grain**  
One row per payment attempt or transaction.

**Entity Type**  
Event.

**Description**  
Represents a payment event against an invoice. Payments are append-only. Retries and failures are recorded as separate rows to preserve full payment history.

**Relationships**  
- References `invoices` via `invoice_id`.

---

## Raw-Layer Ingestion Metadata

All raw tables in the initial schema include ingestion metadata in addition to their business columns:

- `ingest_batch_id`
- `ingested_at`

**Field Definitions**  
- `ingest_batch_id` identifies the batch load that inserted the row.
- `ingested_at` records the timestamp at which the row entered the platform.

**Purpose**  
These fields support ingestion traceability and improve rerun safety, debugging, and reliability testing.