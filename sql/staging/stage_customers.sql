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
    from (
        select
            customer_id,
            customer_name,
            customer_email,
            created_at,
            row_number() over (
                partition by customer_id
                order by created_at desc, customer_name asc
            ) as row_num
        from prepared
    ) ranked
    where row_num = 1

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