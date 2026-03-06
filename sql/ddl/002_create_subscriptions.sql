-- schema version: 002
-- sql/ddl/002_create_subscriptions.sql

create table if not exists subscriptions (
    subscription_id      bigserial primary key,
    customer_id          bigint not null,
    plan_id              bigint not null,
    start_date           date not null,
    end_date             date,
    status               text not null,
    created_at           timestamptz not null default now(),

    constraint fk_subscriptions_customer
        foreign key (customer_id) references customers (customer_id),

    constraint fk_subscriptions_plan
        foreign key (plan_id) references plans (plan_id)
);