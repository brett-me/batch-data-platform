import argparse
import logging
import os
import random

import psycopg


BASE_CUSTOMERS = 100

PLAN_CATALOGUE = [
    ("Basic", 1000),
    ("Pro", 2500),
    ("Enterprise", 7500),
]


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


def seed_customers(cur, rng: random.Random, n_customers: int) -> int:
    # Deterministic, readable customers.
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


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = get_args()

    rng = random.Random(args.seed)
    n_customers = BASE_CUSTOMERS * args.scale

    logging.info("Seed starting (seed=%s scale=%s)", args.seed, args.scale)

    db_config = get_db_config()

    with psycopg.connect(**db_config) as conn:
        with conn.cursor() as cur:
            # Week 1 reset semantics: clear seeded tables and reset identity counters.
            cur.execute("truncate table customers restart identity;")
            cur.execute("truncate table plans restart identity;")

            plans_inserted = seed_plans(cur)
            customers_inserted = seed_customers(cur, rng, n_customers)

        conn.commit()

    logging.info("Seed complete: plans=%s customers=%s", plans_inserted, customers_inserted)


if __name__ == "__main__":
    main()