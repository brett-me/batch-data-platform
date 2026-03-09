-- sql/staging/stage_customers.sql

with source as (

    select
        customer_id,
        customer_name,
        customer_email,
        created_at
    from customers

),

prepared as (

    select
        customer_id,
        customer_name,
        customer_email,
        created_at
    from source

),

final as (

    select
        customer_id,
        customer_name,
        customer_email,
        created_at
    from prepared

)

select
    customer_id,
    customer_name,
    customer_email,
    created_at
from final;