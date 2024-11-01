import pandas as pd
import os

def get_stock_list(input_file_name):
    directory_ = os.path.join(os.getcwd(), "inputs")
    path_file = os.path.join(directory_, input_file_name)

    data = pd.read_csv(path_file)
    data=data.head()
    data=data['Ticker']

    # Add ".NS" to each element in the list
    updated_data_list = [f"{item}.NS" for item in data]
    return updated_data_list