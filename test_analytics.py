from src.analytics import what_if_revenue

def test_what_if():
    result = what_if_revenue(1000, 10)
    assert result["projected_revenue"] == 1100
    assert result["incremental_revenue"] == 100
