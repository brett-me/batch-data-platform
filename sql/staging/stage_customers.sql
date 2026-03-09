-- sql/staging/stage_customers.sql

with source as (
    select
        customer_id,
        customer_name,
        customer_email,
        created_at
    from customers
),

final as (
    select
        customer_id,
        customer_name,
        customer_email,
        created_at
    from source
)

select
    customer_id,
    customer_name,
    customer_email,
    created_at
from final;