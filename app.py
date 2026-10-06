import streamlit as st
from src.agent import AnalystAgent
from src.database import init_database
from src.quality import profile_database

st.set_page_config(page_title="AI Data Analyst Copilot", page_icon="📊", layout="wide")

init_database()

st.title("📊 AI Data Analyst Copilot")
st.caption("Ask business questions in natural language. Get SQL, data, charts and insights.")

with st.sidebar:
    st.header("Data")
    if st.button("Refresh database"):
        init_database(force=True)
        st.success("Database refreshed.")

    st.subheader("Data quality")
    profile = profile_database()
    for table, info in profile.items():
        st.write(f"**{table}** — {info['rows']:,} rows")

question = st.text_area(
    "Ask a business question",
    placeholder="Example: Which product categories generated the most revenue?",
    height=100,
)

if st.button("Analyze", type="primary") and question.strip():
    agent = AnalystAgent()
    with st.spinner("Analyzing..."):
        result = agent.run(question.strip())

    if result.error:
        st.error(result.error)
    else:
        tab1, tab2, tab3 = st.tabs(["📈 Analysis", "🧾 SQL", "🔍 Data"])

        with tab1:
            st.subheader("Business insight")
            st.markdown(result.insight)
            if result.chart is not None:
                st.plotly_chart(result.chart, use_container_width=True)

        with tab2:
            st.code(result.sql, language="sql")

        with tab3:
            st.dataframe(result.data, use_container_width=True)

        st.download_button(
            "Download results as CSV",
            result.data.to_csv(index=False).encode("utf-8"),
            "analysis_results.csv",
            "text/csv",
        )
elif not question.strip():
    st.info("Try: **What are the top 10 products by revenue?**")
