from batch_data_platform.config import PLAN_CATALOGUE, get_db_config
from batch_data_platform.smoke_checks import get_missing_tables


def test_plan_catalogue_is_defined():
    assert len(PLAN_CATALOGUE) == 3
    assert PLAN_CATALOGUE[0] == ("Basic", 1000)
    assert PLAN_CATALOGUE[1] == ("Pro", 2500)
    assert PLAN_CATALOGUE[2] == ("Enterprise", 7500)


def test_get_db_config_defaults(monkeypatch):
    monkeypatch.delenv("DB_HOST", raising=False)
    monkeypatch.delenv("DB_PORT", raising=False)
    monkeypatch.delenv("DB_NAME", raising=False)
    monkeypatch.delenv("DB_USER", raising=False)
    monkeypatch.delenv("DB_PASSWORD", raising=False)

    config = get_db_config()

    assert config == {
        "host": "localhost",
        "port": 5432,
        "dbname": "postgres",
        "user": "postgres",
        "password": "postgres",
    }


def test_get_missing_tables_returns_difference():
    found = {"customers", "plans"}
    missing = get_missing_tables(found)

    assert missing == {"subscriptions", "invoices", "payments"}