# pages/2_Manual_Data_Entry.py
import streamlit as st
import pandas as pd
import io
import altair as alt

st.set_page_config(layout="wide")
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
    value="Date,Open,High,Low,Close\n2025-07-01,82500,82750,82400,82600\n2025-07-02,82600,82900,82550,82800\n2025-07-03,82800,83000,82700,82950\n2025-07-04,82950,83200,82900,83100\n2025-07-07,83100,83350,83000,83250\n2025-07-08,83250,83400,83100,83300\n2025-07-09,83300,83500,83200,83450\n2025-07-10,83450,83600,83350,83550\n2025-07-11,83550,83800,83400,83700\n2025-07-14,83700,83950,83650,83850\n2025-07-15,83850,84100,83700,84000\n2025-07-16,84000,84200,83900,84150\n2025-07-17,84150,84300,84000,84200\n2025-07-18,84200,84400,84100,84350\n2025-07-21,84350,84500,84250,84450\n2025-07-22,84450,84600,84300,84500\n2025-07-23,84500,84700,84400,84650\n2025-07-24,84650,84800,84500,84750\n2025-07-25,84750,84900,84600,84800\n2025-07-28,84800,84950,84700,84850\n2025-07-29,84850,84900,84750,84800\n2025-07-30,84800,84850,84650,84700\n2025-07-31,84700,84750,84550,84600\n2025-08-01,84600,84650,84450,84500\n2025-08-04,84500,84550,84300,84400"
)

if st.button("Create Table & Analyze"):
    if data_input:
        try:
            df = pd.read_csv(io.StringIO(data_input))
            
            # Ensure 'Date' column is in datetime format
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)

            st.success("Table created successfully!")
            
            if 'Close' in df.columns:
                
                # --- NEW CHARTING AND ANALYSIS CODE STARTS HERE ---
                st.subheader("📈 Interactive Charts")
                
                # Candlestick Chart (requires Open, High, Low, Close)
                if all(col in df.columns for col in ['Open', 'High', 'Low', 'Close']):
                    
                    # Create a base chart
                    base = alt.Chart(df.reset_index()).encode(
                        x=alt.X('Date', axis=alt.Axis(format="%Y-%m-%d"))
                    ).properties(
                        title="Candlestick Chart"
                    )
                    
                    # Candlestick body
                    candlestick = base.mark_rule().encode(
                        y=alt.Y('Low', title='Price'),
                        y2='High'
                    ) + base.mark_bar(
                        size=20
                    ).encode(
                        y='Open',
                        y2='Close',
                        color=alt.condition(
                            alt.datum.Open < alt.datum.Close,
                            alt.value('green'),
                            alt.value('red')
                        )
                    )
                    st.altair_chart(candlestick, use_container_width=True)

                # Trend analysis (line chart)
                st.subheader("📊 Trend Analysis & Visualization")
                st.write("A 20-day Simple Moving Average (SMA) has been calculated and visualized to help identify the trend.")
                
                df['20_Day_SMA'] = df['Close'].rolling(window=20).mean()
                
                # Create a DataFrame for charting
                chart_df = df[['Close', '20_Day_SMA']].reset_index().melt('Date', var_name='Metric', value_name='Price')
                
                # Create a line chart with Altair
                line_chart = alt.Chart(chart_df).mark_line().encode(
                    x=alt.X('Date', axis=alt.Axis(format="%Y-%m-%d")),
                    y='Price',
                    color=alt.Color('Metric', legend=alt.Legend(title="Indicator"))
                ).properties(
                    title="Closing Price vs. 20-Day SMA"
                ).interactive()
                
                st.altair_chart(line_chart, use_container_width=True)

                # Display the table with the new column
                st.subheader("Data Table with Analysis")
                st.dataframe(df)

                # Provide a simple trend summary
                latest_close = df['Close'].iloc[-1]
                latest_sma = df['20_Day_SMA'].iloc[-1]
                
                st.write("---")
                st.write("### Trend Summary")
                st.write(f"Latest Closing Price: **{latest_close:.2f}**")
                st.write(f"Latest 20-Day SMA: **{latest_sma:.2f}**")
                
                if latest_close > latest_sma:
                    st.success("Conclusion: The short-term trend is currently **bullish** (above the moving average).")
                else:
                    st.warning("Conclusion: The short-term trend is currently **bearish** (below the moving average).")

                # Provide a download button for the new DataFrame with analysis
                csv_data = df.to_csv().encode('utf-8')
                st.download_button(
                    label="Download Table with Analysis as CSV",
                    data=csv_data,
                    file_name="manual_data_with_analysis.csv",
                    mime="text/csv"
                )
            else:
                st.warning("The 'Close' column was not found. Charts and analysis could not be performed. Please ensure your data has 'Open', 'High', 'Low', and 'Close' columns.")
                st.dataframe(df) # Still show the raw dataframe
                csv_data = df.to_csv().encode('utf-8')
                st.download_button(
                    label="Download Raw Table as CSV",
                    data=csv_data,
                    file_name="manual_data_table.csv",
                    mime="text/csv"
                )
        except Exception as e:
            st.error(f"Error processing data: {e}")
            st.error("Please ensure your data is correctly formatted as comma-separated values (CSV) with a header row.")
    else:
        st.warning("Please paste some data to create a table.")
