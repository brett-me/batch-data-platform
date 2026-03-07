import random
from datetime import date, timedelta

from batch_data_platform.config import (
    BASE_INVOICES_PER_SUBSCRIPTION,
    DUPLICATE_RATE,
    LATE_RATE,
    PLAN_CATALOGUE,
    UNPAID_RATE,
)


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