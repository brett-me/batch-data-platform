import argparse
import logging
import os
import random

import psycopg

from batch_data_platform.config import (
    BASE_CUSTOMERS,
    BASE_SUBSCRIPTIONS,
    get_db_config,
)
from batch_data_platform.seeding import (
    get_plan_prices,
    seed_customers,
    seed_invoices_and_payments,
    seed_plans,
    seed_subscriptions,
)


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed synthetic platform data")
    parser.add_argument("--seed", type=int, default=int(os.getenv("SEED", "123")))
    parser.add_argument("--scale", type=int, default=int(os.getenv("SCALE", "1")))
    return parser.parse_args()


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
            invoices_inserted, payments_inserted, unpaid_invoices, late_payments = (
                seed_invoices_and_payments(cur, rng, plan_prices)
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