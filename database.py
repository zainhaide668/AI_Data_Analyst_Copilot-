from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, inspect, text
from src.config import DATABASE_URL

ENGINE = create_engine(DATABASE_URL)

DATA_DIR = Path("data")

def init_database(force: bool = False) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    db_file = DATA_DIR / "analytics.db"
    if DATABASE_URL.startswith("sqlite:///") and db_file.exists() and not force:
        return
    if force and db_file.exists():
        db_file.unlink()

    from scripts.seed_database import generate_data
    tables = generate_data()
    for name, df in tables.items():
        df.to_sql(name, ENGINE, if_exists="replace", index=False)

def get_schema() -> str:
    inspector = inspect(ENGINE)
    parts = []
    for table in inspector.get_table_names():
        cols = inspector.get_columns(table)
        parts.append(
            f"TABLE {table}:\n" +
            "\n".join(f"  - {c['name']} ({c['type']})" for c in cols)
        )
    return "\n\n".join(parts)

def query_df(sql: str) -> pd.DataFrame:
    with ENGINE.connect() as conn:
        return pd.read_sql(text(sql), conn)
