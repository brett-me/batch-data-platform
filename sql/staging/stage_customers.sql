-- sql/staging/stage_customers.sql

with source as (

    select *
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

deduped as (

    select
        customer_id,
        customer_name,
        customer_email,
        created_at
    from prepared

),

final as (

    select
        customer_id,
        customer_name,
        customer_email,
        created_at
    from deduped

)

select 
    customer_id,
    customer_name,
    customer_email,
    created_at
from final;