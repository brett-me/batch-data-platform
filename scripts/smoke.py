import logging

import psycopg

from batch_data_platform.config import get_db_config
from batch_data_platform.smoke_checks import get_missing_tables


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

    missing_tables = get_missing_tables(found_tables)

    if missing_tables:
        raise RuntimeError(
            f"Smoke check failed: missing expected tables: {sorted(missing_tables)}"
        )

    logging.info("Smoke check passed: database reachable and expected tables exist")


if __name__ == "__main__":
    main()