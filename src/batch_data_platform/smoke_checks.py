EXPECTED_TABLES = {
    "customers",
    "plans",
    "subscriptions",
    "invoices",
    "payments",
}


def get_missing_tables(found_tables: set[str]) -> set[str]:
    return EXPECTED_TABLES - found_tables