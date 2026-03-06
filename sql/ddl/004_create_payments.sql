-- sql/ddl/004_create_payments.sql

create table if not exists payments (
    payment_id        bigserial primary key,
    invoice_id        bigint not null,
    amount_paid_cents integer not null,
    paid_at           date not null,
    status            text not null,
    created_at        timestamptz not null default now(),

    constraint fk_payments_invoice
        foreign key (invoice_id) references invoices (invoice_id)
);