import logging
import os

import psycopg


EXPECTED_TABLES = {
    "customers",
    "plans",
    "subscriptions",
    "invoices",
    "payments",
}


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
    db_config = get_db_config()

    with psycopg.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                select table_name
                from information_schema.tables
                where table_schema = 'public'
                """
            )
            found_tables = {row[0] for row in cur.fetchall()}

    missing_tables = EXPECTED_TABLES - found_tables

    if missing_tables:
        raise RuntimeError(
            f"Smoke check failed: missing expected tables: {sorted(missing_tables)}"
        )

    logging.info("Smoke check passed: database reachable and expected tables exist")


if __name__ == "__main__":
    main()