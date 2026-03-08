# Local Rebuild Validation

## Objective

Validate that the platform can be rebuilt from a clean local state using the documented repository interface.

## Validation Flow

The following commands were executed from the repository root:

```bash
cp .env.example .env
make dev-install
make up
make status
make smoke
make ddl
make smoke
make seed
make checks
make psql
make down
make test
make lint
```

## Results by Step

### `cp .env.example .env`

Succeeded as expected.

### `make dev-install`

Succeeded.

Observation:

- local installation defaulted to user scope because the normal site-packages directory was not writeable

### `make up`

Succeeded as expected.

### `make status`

Succeeded as expected.

Observation:

- useful for confirming container state immediately after `make up`

### `make smoke`

Failed before schema application.

Output indicated that expected tables were missing:

- `customers`
- `plans`
- `subscriptions`
- `invoices`
- `payments`

This behaviour was consistent with the current implementation, because the smoke check validates both:

- database reachability
- expected table existence

At this point in the rebuild flow, the schema had not yet been applied.

### `make ddl`

Succeeded as expected.

### `make smoke` (after `make ddl`)

Succeeded.

Output confirmed:

- database reachable
- expected tables exist

### `make seed`

Succeeded as expected.

### `make checks`

Succeeded as expected.

### `make psql`

Succeeded as expected.

### `make down`

Succeeded as expected.

### `make test`

Succeeded as expected.

### `make lint`

Succeeded as expected.

## Overall Result

The platform was successfully rebuilt from a clean local state.

Schema application, seeding, sanity checks, unit tests, and lint checks all completed successfully once the schema had been applied.

## Issues Identified

### Smoke check ordering in README

The documented Quickstart placed `make smoke` before `make ddl`.

Because the smoke check validates the existence of expected tables, this ordering caused the command to fail before schema application.

This was a documentation and workflow-order issue, not a defect in the smoke check itself.

### `make dev-install` user-install message

The following message appeared during local dependency installation:

> Defaulting to user installation because normal site-packages is not writeable

This did not block execution. It is a local environment note and may be documented separately if it appears consistently across setups.

### Repository structure presentation

The README structure tree was accurate but could be presented in a more workflow-oriented order.

## Changes Implemented as a Result of Validation

The repository was updated to reflect the rebuild findings:

- the README Quickstart flow was corrected so that `make ddl` runs before `make smoke`
- the clean-room rebuild sequence was aligned with the current smoke-check behaviour
- troubleshooting guidance was expanded to explain smoke-check ordering, password handling, and reset semantics
- configuration documentation was clarified to better describe the local configuration contract
- Make targets were refined to load `.env` consistently for database-related commands

These changes are reflected in the current repository state.

## Operational Notes

- `make reset` recreates the local PostgreSQL container and removes the local database volume.
- `make smoke` should be run after `make ddl`, because the smoke check expects the schema tables to exist.
- `make checks` is designed to fail loudly if seeded data does not meet the required sanity conditions.

## Conclusion

The documented local rebuild workflow is valid for the current repository state.

The platform can be recreated from a known clean state using the documented commands without requiring undocumented recovery steps.

Validation evidence for row counts, orphan checks, unpaid invoices, and late payments is enforced through make checks via sql/checks/001_sanity.sql.
