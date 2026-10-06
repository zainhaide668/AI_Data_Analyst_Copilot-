import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def revenue_column(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if {"quantity", "unit_price"}.issubset(out.columns):
        out["revenue"] = out["quantity"] * out["unit_price"]
    return out

def what_if_revenue(current_revenue: float, increase_pct: float) -> dict:
    projected = current_revenue * (1 + increase_pct / 100)
    return {
        "current_revenue": current_revenue,
        "increase_pct": increase_pct,
        "projected_revenue": projected,
        "incremental_revenue": projected - current_revenue,
    }

def forecast(values: pd.Series, periods: int = 3) -> pd.Series:
    values = pd.Series(values).dropna().astype(float)
    if len(values) < 4:
        raise ValueError("At least four observations are required.")
    model = ExponentialSmoothing(values, trend="add", seasonal=None)
    return model.fit(optimized=True).forecast(periods)
