from pathlib import Path
import random
import pandas as pd

def generate_data(seed=42):
    random.seed(seed)

    regions = ["North", "South", "East", "West"]
    categories = {
        "Electronics": [("Wireless Headphones", 79.0), ("Keyboard", 42.0), ("Monitor", 219.0)],
        "Home": [("Desk Lamp", 35.0), ("Office Chair", 159.0), ("Water Bottle", 18.0)],
        "Accessories": [("Backpack", 55.0), ("USB Cable", 12.0), ("Mouse", 28.0)],
    }

    products = []
    pid = 1001
    for category, items in categories.items():
        for name, price in items:
            products.append({"product_id": pid, "name": name, "category": category, "price": price})
            pid += 1

    customers = []
    for cid in range(1, 101):
        customers.append({
            "customer_id": cid,
            "name": f"Customer {cid:03d}",
            "gender": random.choice(["F", "M"]),
            "region": random.choice(regions),
            "segment": random.choice(["Consumer", "SMB", "Enterprise"]),
        })

    dates = pd.date_range("2025-01-01", "2026-09-30", freq="D")
    orders = []
    oid = 1
    for _ in range(1800):
        date = random.choice(dates)
        cid = random.randint(1, 100)
        product = random.choice(products)
        qty = random.randint(1, 5)
        orders.append({
            "order_id": oid,
            "customer_id": cid,
            "order_date": date.date().isoformat(),
            "product_id": product["product_id"],
            "quantity": qty,
            "unit_price": product["price"],
        })
        oid += 1

    return {
        "customers": pd.DataFrame(customers),
        "products": pd.DataFrame(products),
        "orders": pd.DataFrame(orders),
    }

if __name__ == "__main__":
    from src.database import ENGINE
    for name, df in generate_data().items():
        df.to_sql(name, ENGINE, if_exists="replace", index=False)
    print("Sample database created at data/analytics.db")
