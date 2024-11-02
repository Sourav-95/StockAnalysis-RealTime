from StockIngestion import StockFeatureEngineering, StockInfoFetcher
from src_comp.logger import logger
import sys
import pandas as pd

from src.stock_list import get_stock_list
sys.path.append('G:\StockAnalysis_API\StockAnalysis-RealTime')

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def main(stock_name):
    """Main function to execute the stock fetching and analysis."""
    try:
        stock_info_fetcher = StockInfoFetcher(stock_name)
        data_all_info = stock_info_fetcher.filter_stock_info()

        # Check if the resulting DataFrame contains valid data
        if data_all_info.empty or data_all_info.isna().all(axis=None):  # Check if DataFrame is empty or all NaN
            logger.warning(f"No valid data found for {stock_name}.")
            return None

        stock_analyzer = StockFeatureEngineering(stock_info_fetcher.stock, data_all_info)
        result = stock_analyzer.StockFeatureEngine()
        logger.info(f"Result fetched & stored for {stock_name}.\n")
        return result
    except ValueError as ve:
        # Handle specific known error, e.g., stock not found
        logger.error(f"ValueError: {ve} for stock {stock_name}")
        return None
    except Exception as e:
        # Log the exception and return None for any other errors
        logger.error(f"Error occurred while processing {stock_name}: {e}")
        return None


# Run the main function and log output
if __name__ == "__main__":
    # Uploading the CSV of Stock list
    stock_list = get_stock_list(input_file_name='stock_list.csv')
    logger.info(f'Total no of Records for which need to fetch Stock Details are: {len(stock_list)}\n\n')

    final_df = pd.DataFrame()

    for item in stock_list:
        main_df = main(item)
        
        # Only concatenate if main_df is not None and contains valid data
        if main_df is None or not isinstance(main_df, pd.DataFrame):
            logger.warning(f'No valid data returned for {item}. Skipping this stock.')
            continue  # Skip to the next iteration
        else:
            final_df = pd.concat([final_df, main_df], ignore_index=True)
            logger.info(f'All Details Fetched & stored for {item}')

    logger.info(f'Total records in the final DataFrame: {final_df.shape[0]}')
    print(final_df)
