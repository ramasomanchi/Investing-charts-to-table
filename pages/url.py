# pages/1_URL_Input.py
import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide")
st.title("🔗 Extract Data from URL")
st.write("Enter a URL below. The app will attempt to find and display any standard HTML tables on that page.")
st.write("*(Note: This works best for pages with explicit HTML tables, not for data rendered dynamically by JavaScript charts.)*")

url_input = st.text_input(
    "Enter the URL:",
    "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)" # Using a good example URL
)

if st.button("Fetch Tables"):
    if url_input:
        with st.spinner("Fetching and parsing tables... This might take a moment."):
            try:
                # Add a User-Agent header to mimic a web browser
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                # Fetch the page content with the headers
                response = requests.get(url_input, headers=headers)
                response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx or 5xx)

                # Use pandas to read HTML tables from the fetched content
                tables = pd.read_html(response.text)

                if tables:
                    st.success(f"Found {len(tables)} table(s) on the page!")
                    for i, df in enumerate(tables):
                        st.subheader(f"Table {i+1}")
                        st.dataframe(df)

                        csv_data = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label=f"Download Table {i+1} as CSV",
                            data=csv_data,
                            file_name=f"table_{i+1}.csv",
                            mime="text/csv",
                            key=f"download_table_{i+1}"
                        )
                        st.markdown("---")
                else:
                    st.warning("No HTML tables found on this URL. Please ensure the data is in a standard HTML table format.")
            except requests.exceptions.RequestException as e:
                st.error(f"An HTTP error occurred: {e}")
                st.error("The website might be blocking requests or the URL is invalid.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.error("Could not fetch or parse tables. This could be due to the website structure or other issues.")
    else:
        st.warning("Please enter a URL to fetch tables.")
