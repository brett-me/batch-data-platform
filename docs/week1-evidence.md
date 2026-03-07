# Week 1 Evidence

## Day 6 - Clean-room Simulation

### Objective

Validate that the repository can be rebuilt from a clean local state using only the documented interface and workflow.

### Commands Run

- `cp .env.example .env`
- `make dev-install`
- `make up`
- `make status`
- `make smoke`
- `make ddl`
- `make smoke`
- `make seed`
- `make checks`
- `make psql`
- `make down`
- `make test`
- `make lint`

### Results by Step

#### `cp .env.example .env`
Succeeded as expected.

#### `make dev-install`
Succeeded.

Observation:
- local installation defaulted to user scope because the normal site-packages directory was not writeable

#### `make up`
Succeeded as expected.

#### `make status`
Succeeded as expected.

Observation:
- useful for confirming container state immediately after `make up`

#### `make smoke`
Failed before schema application.

Output indicated that expected tables were missing:
- `customers`
- `plans`
- `subscriptions`
- `invoices`
- `payments`

This behaviour is technically correct, because the smoke check currently validates both:
- database reachability
- expected table existence

At this point in the rebuild flow, the schema had not yet been applied.

#### `make ddl`
Succeeded as expected.

#### `make smoke` (after `make ddl`)
Succeeded.

Output confirmed:
- database reachable
- expected tables exist

#### `make seed`
Succeeded as expected.

#### `make checks`
Succeeded as expected.

#### `make psql`
Succeeded as expected.

#### `make down`
Succeeded as expected.

#### `make test`
Succeeded as expected.

#### `make lint`
Succeeded as expected.

## Overall Result

The platform was successfully rebuilt from a clean local state.

The schema, seed, checks, tests, and lint workflow all completed successfully once the schema had been applied.

The clean-room simulation therefore passed, with one important workflow clarification identified around the smoke check.

## Friction Identified

### 1. Smoke check appears too early in the README flow
The current Quickstart places `make smoke` before `make ddl`.

In the current implementation, `make smoke` checks for:
- database reachability
- existence of expected tables

Because the tables do not yet exist before `make ddl`, the command fails at that point in the documented sequence.

This is not a bug in the smoke check itself. It is a mismatch between:
- what the smoke check currently validates
- where it appears in the Quickstart flow

### 2. `make dev-install` may produce a user-install message
The message:

> Defaulting to user installation because normal site-packages is not writeable

did not block execution, but it is a useful note for local development behaviour in WSL.

This may be worth documenting later in a runbook or troubleshooting note if it appears consistently.

### 3. Repository structure presentation could better reflect workflow order
The current README structure tree is accurate, but not necessarily ordered according to how the repository is used.

A more workflow-oriented structure presentation may improve readability.

## Fixes / Follow-up Actions

### Recommended
- Move `make smoke` to **after** `make ddl` in the Quickstart flow, if the smoke check is intended to validate both connectivity and schema presence.

### Optional
- Document the possible `pip` user-install message in a troubleshooting or runbook note if it is consistently observed.
- Consider reordering the README structure tree so it better reflects operational and development flow.

## Notes

The clean-room simulation was valuable because it exposed a workflow mismatch that would be easy to miss during normal development. The platform itself behaved correctly, but the README sequence should be adjusted so that the documented happy path matches the actual behaviour of the smoke check.
