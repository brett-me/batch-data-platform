-- schema version: 003
-- sql/ddl/003_create_invoices.sql

create table if not exists invoices (
    invoice_id            bigserial primary key,
    subscription_id       bigint not null,
    billing_period_start  date not null,
    billing_period_end    date not null,
    amount_due_cents      integer not null,
    issued_at             date not null,
    due_date              date not null,
    status                text not null,
    created_at            timestamptz not null default now(),

    constraint fk_invoices_subscription
        foreign key (subscription_id) references subscriptions (subscription_id)
);