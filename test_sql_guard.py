import pytest
from src.sql_guard import validate_sql

def test_select_is_allowed():
    assert validate_sql("SELECT * FROM customers").startswith("SELECT")

def test_write_is_blocked():
    with pytest.raises(ValueError):
        validate_sql("DROP TABLE customers")

def test_multiple_statements_blocked():
    with pytest.raises(ValueError):
        validate_sql("SELECT * FROM customers; DELETE FROM customers")
