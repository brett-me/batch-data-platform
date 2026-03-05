import argparse
import logging
import os
import random

import psycopg


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


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = get_args()

    rng = random.Random(args.seed)
    logging.info("Seed script starting")
    logging.info("seed=%s scale=%s sample_random=%s", args.seed, args.scale, rng.randint(1, 100))

    db_config = get_db_config()

    with psycopg.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute("select current_database(), current_user;")
            db_name, db_user = cur.fetchone()

    logging.info("Connected successfully to database=%s as user=%s", db_name, db_user)
    logging.info("Seed skeleton complete")


if __name__ == "__main__":
    main()