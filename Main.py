# main.py
import streamlit as st

st.set_page_config(
    page_title="Chart to Table Converter",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Chart Data to Downloadable Table")

st.markdown("""
Welcome! This app helps you convert data from charts or other sources into a downloadable table.

You have two main options:

1.  **Extract from a URL:** Provide a URL, and the app will try to find HTML tables on that page.
2.  **Enter Data Manually:** If you have a screenshot or want to type data directly, use this option.

Use the sidebar to navigate between options.
""")

st.info("💡 **Note on Chart Conversion:** Directly extracting data from complex live charts (like candlestick charts from images or dynamic websites) is a very advanced task requiring specialized AI/ML. This app focuses on extracting from existing HTML tables or manual input.")

# Add a simple footer
st.markdown("---")
st.markdown("Developed with ❤️ by Ramalakshmi")
