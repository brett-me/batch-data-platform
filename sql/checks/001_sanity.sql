-- sql/checks/001_sanity.sql

-- row counts
select 'customers' as table_name, count(*) as row_count from customers
union all
select 'plans', count(*) from plans
union all
select 'subscriptions', count(*) from subscriptions
union all
select 'invoices', count(*) from invoices
union all
select 'payments', count(*) from payments
;

-- unpaid invoices should exist (for later drills)
select count(*) as unpaid_invoices
from invoices
where status = 'unpaid'
;

-- late payments should exist (for later drills)
select count(*) as late_payments
from payments p
join invoices i on i.invoice_id = p.invoice_id
where p.paid_at > i.due_date
;

-- foreign key integrity checks (should return 0)
select count(*) as invoices_missing_subscription
from invoices i
left join subscriptions s on s.subscription_id = i.subscription_id
where s.subscription_id is null
;

select count(*) as payments_missing_invoice
from payments p
left join invoices i on i.invoice_id = p.invoice_id
where i.invoice_id is null
;