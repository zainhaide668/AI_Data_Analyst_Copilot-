import re

FORBIDDEN = {
    "insert", "update", "delete", "drop", "alter", "create",
    "attach", "detach", "pragma", "vacuum", "replace", "truncate"
}

def validate_sql(sql: str) -> str:
    cleaned = sql.strip().strip("`")
    cleaned = re.sub(r"^sql\s*", "", cleaned, flags=re.I).strip()

    if not cleaned:
        raise ValueError("Empty SQL query.")

    if ";" in cleaned.rstrip(";"):
        raise ValueError("Multiple SQL statements are not allowed.")

    first = cleaned.split(None, 1)[0].lower()
    if first not in {"select", "with"}:
        raise ValueError("Only SELECT/WITH queries are allowed.")

    lowered = cleaned.lower()
    for word in FORBIDDEN:
        if re.search(rf"\b{re.escape(word)}\b", lowered):
            raise ValueError(f"Forbidden SQL operation: {word}")

    if " limit " not in f" {lowered} ":
        cleaned = cleaned.rstrip(";") + " LIMIT 500"

    return cleaned
