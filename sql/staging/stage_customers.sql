-- sql/staging/stage_customers.sql

with source as (

    select
        customer_id,
        customer_name,
        customer_email,
        created_at
    from customers

),

standardized as (

    select
        customer_id,
        customer_name as name,
        customer_email as email,
        created_at
    from source

),

final as (

    select
        customer_id,
        name,
        email,
        created_at
    from standardized

)

select
    customer_id,
    name,
    email,
    created_at
from final;