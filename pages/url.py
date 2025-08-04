# pages/1_URL_Input.py
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide") # Ensure consistent wide layout
st.title("🔗 Extract Data from URL")
st.write("Enter a URL below. The app will attempt to find and display any standard HTML tables on that page.")
st.write("*(Note: This works best for pages with explicit HTML tables, not for data rendered dynamically by JavaScript charts.)*")

url_input = st.text_input("Enter the URL:", "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)")

if st.button("Fetch Tables"):
    if url_input:
        with st.spinner("Fetching and parsing tables... This might take a moment."):
            try:
                # Use pandas to read HTML tables from the URL
                tables = pd.read_html(url_input)

                if tables:
                    st.success(f"Found {len(tables)} table(s) on the page!")
                    for i, df in enumerate(tables):
                        st.subheader(f"Table {i+1}")
                        st.dataframe(df)

                        # Provide download button for each table
                        csv_data = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label=f"Download Table {i+1} as CSV",
                            data=csv_data,
                            file_name=f"table_{i+1}.csv",
                            mime="text/csv",
                            key=f"download_table_{i+1}"
                        )
                        st.markdown("---") # Separator
                else:
                    st.warning("No HTML tables found on this URL. Please ensure the data is in a standard HTML table format.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.error("Could not fetch or parse tables. This could be due to network issues, website structure, or dynamic content.")
    else:
        st.warning("Please enter a URL to fetch tables.")
