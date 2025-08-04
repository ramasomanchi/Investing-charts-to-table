# pages/2_Manual_Data_Entry.py
import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide") # Ensure consistent wide layout
st.title("✍️ Enter Data Manually (from Screenshot/Observation)")
st.write("If you have data from a screenshot or any other source, paste it below. Make sure it's in a comma-separated format (CSV style), with the first line being headers.")
st.write("Example:")
st.code("""
Date,Open,High,Low,Close
2025-07-28,81075.00,82050.00,81025.00,81850.00
2025-07-29,81850.00,82150.00,81400.00,81600.00
2025-07-30,81600.00,82300.00,81550.00,82100.00
""")

data_input = st.text_area(
    "Paste your data here (CSV format):",
    height=300,
    value="Date,Open,High,Low,Close\n2025-08-01,81018.72,81500.00,80800.00,81200.00\n2025-08-02,81200.00,81800.00,81100.00,81750.00"
)

if st.button("Create Table"):
    if data_input:
        try:
            # Read the text input as if it's a CSV file
            df = pd.read_csv(io.StringIO(data_input))
            st.success("Table created successfully!")
            st.dataframe(df)

            # Provide download button
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Table as CSV",
                data=csv_data,
                file_name="manual_data_table.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Error processing data: {e}")
            st.error("Please ensure your data is correctly formatted as comma-separated values (CSV) with a header row.")
    else:
        st.warning("Please paste some data to create a table.")
