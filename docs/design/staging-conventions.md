# Staging Conventions

Apply these conventions to all staging models.

## Naming

- Use full-word model names, for example `stage_customers.sql`.
- Use lower `snake_case` for model names, CTE names, aliases, and staged column names.
- Do not use quoted identifiers.

## Baseline shape

Default staged-model shape:

- `source`
- `standardized`
- `final`

Use only the CTEs the model actually needs.

## Column handling

- Project columns explicitly.
- Do not use `select *`.
- Rename and recast to project conventions in `standardized`.
- Publish the staged entity shape in `final`.
- Use cleaner entity-facing column names in staging where appropriate, for example:
  - `customer_name` -> `name`
  - `customer_email` -> `email`

## Extension rules

After `standardized`, add only functional CTEs that perform one clear unit of work, for example:

- `filtered`
- `derived`
- `deduped`

Use `deduped` only when the model requires survivorship logic.

## Baseline template

```sql
with source as (

    select
        ...
    from ...

),

standardized as (

    select
        ... -- rename and recast to project conventions
    from source

),

final as (

    select
        ...
    from standardized

)

select
    ...
from final;