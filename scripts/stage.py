import logging

import psycopg

from batch_data_platform.config import get_db_config
from batch_data_platform.staging import (
    build_stage_view_sql,
    get_stage_model_files,
    get_view_name,
)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    model_files = get_stage_model_files()
    if not model_files:
        raise RuntimeError("No staging SQL files found in sql/staging/")

    db_config = get_db_config()

    with psycopg.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute("create schema if not exists staging;")

            for model_file in model_files:
                view_name = get_view_name(model_file)
                model_sql = model_file.read_text(encoding="utf-8")
                ddl_sql = build_stage_view_sql(view_name=view_name, model_sql=model_sql)

                cur.execute(ddl_sql)
                logging.info("Built staging view: staging.%s", view_name)

        conn.commit()


if __name__ == "__main__":
    main()