-- sql/staging/stage_plans.sql

with source as (

    select
        plan_id,
        plan_name,
        default_price_cents,
        created_at
    from plans

),

standardized as (

    select
        plan_id,
        plan_name as name,
        default_price_cents,
        created_at
    from source

),

final as (

    select
        plan_id,
        name,
        default_price_cents,
        created_at
    from standardized

)

select
    plan_id,
    name,
    default_price_cents,
    created_at
from final;