from dataclasses import dataclass
import pandas as pd
from src.database import get_schema, query_df
from src.sql_guard import validate_sql
from src.prompts import SQL_SYSTEM, INSIGHT_SYSTEM
from src.llm import ask
from src.charts import auto_chart
from src.config import OPENAI_API_KEY

@dataclass
class Result:
    sql: str = ""
    data: pd.DataFrame = None
    chart: object = None
    insight: str = ""
    error: str = ""

class AnalystAgent:
    def run(self, question: str) -> Result:
        try:
            if not OPENAI_API_KEY:
                return self.demo(question)

            sql = ask(SQL_SYSTEM.format(schema=get_schema()), question)
            sql = validate_sql(sql)
            df = query_df(sql)

            insight = ask(
                INSIGHT_SYSTEM,
                f"Question: {question}\nSQL: {sql}\nResult:\n{df.head(100).to_csv(index=False)}"
            )
            return Result(sql=sql, data=df, chart=auto_chart(df), insight=insight)
        except Exception as exc:
            return Result(error=str(exc))

    def demo(self, question: str) -> Result:
        q = question.lower()
        if "top" in q and "product" in q:
            sql = """SELECT p.name AS product,
SUM(o.quantity * o.unit_price) AS revenue
FROM orders o
JOIN products p ON p.product_id = o.product_id
GROUP BY p.name
ORDER BY revenue DESC
LIMIT 10"""
        elif "region" in q:
            sql = """SELECT c.region,
SUM(o.quantity * o.unit_price) AS revenue
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
GROUP BY c.region
ORDER BY revenue DESC
LIMIT 50"""
        else:
            sql = """SELECT order_date,
SUM(quantity * unit_price) AS revenue
FROM orders
GROUP BY order_date
ORDER BY order_date
LIMIT 500"""
        df = query_df(sql)
        return Result(
            sql=sql,
            data=df,
            chart=auto_chart(df),
            insight="Demo mode is active because no LLM API key is configured. Add OPENAI_API_KEY for natural-language SQL and AI-generated insights."
        )
