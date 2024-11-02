import pandas as pd
import os

def get_stock_list(input_file_path, market_country="India"):
    input_file_path = input_file_path.replace("\\", "/")
    
    # Load the data from the specified CSV file path
    data = pd.read_csv(input_file_path)
    data = data.head()  # Get the first few rows if required
    data = data['Ticker']  # Select the 'Ticker' column
    
    # Modify tickers based on market country
    if market_country == "India":
        # Ensure each ticker ends with '.NS'
        updated_data_list = [ticker if ticker.endswith(".NS") else f"{ticker}.NS" for ticker in data]
    else:
        # For other markets, keep tickers unchanged
        updated_data_list = list(data)
    
    return updated_data_list
