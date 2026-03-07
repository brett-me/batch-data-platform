import os

PLAN_CATALOGUE = [
    ("Basic", 1000),
    ("Pro", 2500),
    ("Enterprise", 7500),
]

BASE_CUSTOMERS = 100
BASE_SUBSCRIPTIONS = 130
DUPLICATE_RATE = 0.02

BASE_INVOICES_PER_SUBSCRIPTION = 4
UNPAID_RATE = 0.10
LATE_RATE = 0.05


def get_db_config() -> dict:
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "dbname": os.getenv("DB_NAME", "postgres"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "postgres"),
    }