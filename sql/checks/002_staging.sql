-- sql/checks/002_staging.sql

-- report duplicate customer_ids in staging
select customer_id, count(*) as row_count
from staging.stage_customers
group by customer_id
having count(*) > 1
;

-- fail if duplicate customer_ids exist
do $$
begin
    if exists (
        select 1
        from staging.stage_customers
        group by customer_id
        having count(*) > 1
    ) then
        raise exception 'staging check failed: duplicate customer_id values found in staging.stage_customers';
    end if;
end
$$;

-- fail if customer_id is null
do $$
begin
    if exists (
        select 1
        from staging.stage_customers
        where customer_id is null
    ) then
        raise exception 'staging check failed: null customer_id values found in staging.stage_customers';
    end if;
end
$$;