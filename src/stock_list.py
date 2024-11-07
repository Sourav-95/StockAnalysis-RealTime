import pandas as pd
import os

def get_stock_list_india(input_file_path):
    
    # Load the data from the specified CSV file path
    data = pd.read_csv(input_file_path)
    data = data['Ticker']  # Select the 'Ticker' column
    
    updated_data_list_nse = [ticker if ticker.endswith(".NS") else f"{ticker}.NS" for ticker in data]

    return updated_data_list_nse
