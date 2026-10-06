from src.database import ENGINE
from sqlalchemy import inspect, text

def profile_database():
    inspector = inspect(ENGINE)
    result = {}
    with ENGINE.connect() as conn:
        for table in inspector.get_table_names():
            rows = conn.execute(text(f'SELECT COUNT(*) FROM "{table}"')).scalar()
            result[table] = {"rows": int(rows)}
    return result
