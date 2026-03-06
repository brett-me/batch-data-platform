-- schema version: 001
-- sql/ddl/001_create_core_tables.sql

create table if not exists customers (
    customer_id         bigserial primary key,
    customer_name       text not null,
    customer_email      text,
    created_at          timestamptz not null default now()
);

create table if not exists plans (
    plan_id             bigserial primary key,
    plan_name           text not null,
    default_price_cents integer not null,
    created_at          timestamptz not null default now()
);