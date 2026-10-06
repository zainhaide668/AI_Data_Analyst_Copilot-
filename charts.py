import pandas as pd
import plotly.express as px

def auto_chart(df: pd.DataFrame):
    if df.empty or len(df.columns) < 2:
        return None

    cols = list(df.columns)
    numeric = df.select_dtypes(include="number").columns.tolist()
    categorical = [c for c in cols if c not in numeric]

    if len(numeric) >= 1 and len(categorical) >= 1:
        x, y = categorical[0], numeric[0]
        if len(df) > 30:
            return px.line(df, x=x, y=y, markers=True)
        return px.bar(df, x=x, y=y)

    if len(numeric) >= 2:
        return px.scatter(df, x=numeric[0], y=numeric[1])

    return None
