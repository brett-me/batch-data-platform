import argparse
import logging
import os
import random
from datetime import date, timedelta

import psycopg

BASE_CUSTOMERS = 100

PLAN_CATALOGUE = [
    ("Basic", 1000),
    ("Pro", 2500),
    ("Enterprise", 7500),
]

BASE_SUBSCRIPTIONS = 130
DUPLICATE_RATE = 0.02

BASE_INVOICES_PER_SUBSCRIPTION = 4
UNPAID_RATE = 0.10 
LATE_RATE = 0.05   


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed synthetic platform data")
    parser.add_argument("--seed", type=int, default=int(os.getenv("SEED", "123")))
    parser.add_argument("--scale", type=int, default=int(os.getenv("SCALE", "1")))
    return parser.parse_args()


def get_db_config() -> dict:
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "dbname": os.getenv("DB_NAME", "postgres"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "postgres"),
    }


def seed_plans(cur) -> int:
    cur.executemany(
        """
        insert into plans (plan_name, default_price_cents)
        values (%s, %s)
        """,
        PLAN_CATALOGUE,
    )
    return len(PLAN_CATALOGUE)


def seed_customers(cur, n_customers: int) -> int:
    rows = []
    for i in range(1, n_customers + 1):
        name = f"Customer {i:03d}"
        email = f"customer{i:03d}@example.com"
        rows.append((name, email))

    cur.executemany(
        """
        insert into customers (customer_name, customer_email)
        values (%s, %s)
        """,
        rows,
    )
    return n_customers


def seed_subscriptions(cur, rng: random.Random, n_customers: int, n_subscriptions: int) -> int:
    today = date.today()
    start_window_days = 365

    rows = []
    for _ in range(n_subscriptions):
        customer_id = rng.randint(1, n_customers)
        plan_id = rng.randint(1, len(PLAN_CATALOGUE))

        start_date = today - timedelta(days=rng.randint(0, start_window_days))

        status = "active" if rng.random() < 0.75 else "cancelled"

        end_date = None
        if status == "cancelled":
            days_active = rng.randint(1, 180)
            end_date = start_date + timedelta(days=days_active)
            if end_date > today:
                end_date = today

        rows.append((customer_id, plan_id, start_date, end_date, status))

        # Controlled duplicate: repeat the same logical row sometimes
        if rng.random() < DUPLICATE_RATE:
            rows.append((customer_id, plan_id, start_date, end_date, status))

    cur.executemany(
        """
        insert into subscriptions (customer_id, plan_id, start_date, end_date, status)
        values (%s, %s, %s, %s, %s)
        """,
        rows,
    )
    return len(rows)


def get_plan_prices(cur) -> dict[int, int]:
    cur.execute("select plan_id, default_price_cents from plans;")
    return {int(pid): int(price) for pid, price in cur.fetchall()}


def seed_invoices_and_payments(
    cur, rng: random.Random, plan_prices: dict[int, int]
) -> tuple[int, int, int, int]:
    """
    returns: (invoices_inserted, payments_inserted, unpaid_invoices, late_payments)
    """
    cur.execute("select subscription_id, plan_id, start_date, end_date, status from subscriptions;")
    subs = cur.fetchall()

    invoices_rows = []
    payments_rows = []

    unpaid_count = 0
    late_count = 0

    today = date.today()

    for subscription_id, plan_id, start_date, end_date, status in subs:
        for k in range(BASE_INVOICES_PER_SUBSCRIPTION):
            period_start = start_date + timedelta(days=30 * k)
            period_end = period_start + timedelta(days=29)

            if period_start > today:
                break
            if end_date is not None and period_start > end_date:
                break

            amount_due = plan_prices[int(plan_id)]
            issued_at = period_end
            due_date = issued_at + timedelta(days=14)

            is_unpaid = rng.random() < UNPAID_RATE
            if is_unpaid:
                status_txt = "unpaid"
                unpaid_count += 1
            else:
                status_txt = "paid"

            invoices_rows.append(
                (subscription_id, period_start, period_end, amount_due, issued_at, due_date, status_txt)
            )

            if not is_unpaid:
                is_late = rng.random() < LATE_RATE
                if is_late:
                    paid_at = due_date + timedelta(days=rng.randint(1, 30))
                    late_count += 1
                else:
                    paid_at = issued_at + timedelta(days=rng.randint(0, 10))

                if paid_at > today:
                    paid_at = today

                payments_rows.append(
                    (subscription_id, period_start, issued_at, amount_due, paid_at, "succeeded")
                )

    cur.executemany(
        """
        insert into invoices (
            subscription_id, billing_period_start, billing_period_end,
            amount_due_cents, issued_at, due_date, status
        )
        values (%s, %s, %s, %s, %s, %s, %s)
        """,
        invoices_rows,
    )

    cur.execute(
        """
        select invoice_id, subscription_id, billing_period_start, issued_at
        from invoices
        """
    )
    invoice_id_map = {
        (sid, bps, ia): iid for (iid, sid, bps, ia) in cur.fetchall()
    }

    payment_insert_rows = []
    for sid, bps, ia, amount_due, paid_at, pay_status in payments_rows:
        invoice_id = invoice_id_map[(sid, bps, ia)]
        payment_insert_rows.append((invoice_id, amount_due, paid_at, pay_status))

    cur.executemany(
        """
        insert into payments (invoice_id, amount_paid_cents, paid_at, status)
        values (%s, %s, %s, %s)
        """,
        payment_insert_rows,
    )

    return (len(invoices_rows), len(payment_insert_rows), unpaid_count, late_count)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = get_args()

    rng = random.Random(args.seed)
    n_customers = BASE_CUSTOMERS * args.scale
    n_subscriptions = BASE_SUBSCRIPTIONS * args.scale

    logging.info("Seed starting (seed=%s scale=%s)", args.seed, args.scale)

    db_config = get_db_config()

    with psycopg.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "truncate table payments, invoices, subscriptions, customers, plans restart identity;"
            )

            plans_inserted = seed_plans(cur)
            customers_inserted = seed_customers(cur, n_customers)
            subscriptions_inserted = seed_subscriptions(cur, rng, n_customers, n_subscriptions)

            plan_prices = get_plan_prices(cur)
            invoices_inserted, payments_inserted, unpaid_invoices, late_payments = seed_invoices_and_payments(
                cur, rng, plan_prices
            )

        conn.commit()

    logging.info(
        "Seed complete: plans=%s customers=%s subscriptions=%s invoices=%s payments=%s unpaid_invoices=%s late_payments=%s",
        plans_inserted,
        customers_inserted,
        subscriptions_inserted,
        invoices_inserted,
        payments_inserted,
        unpaid_invoices,
        late_payments,
    )


if __name__ == "__main__":
    main()