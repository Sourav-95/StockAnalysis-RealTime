import os
import sys
import pandas as pd
import warnings
from tqdm import tqdm
from StockIngestion import StockFeatureEngineering, StockInfoFetcher
from src_comp.logger import logger, logger_terminal
from src.stock_list import get_stock_list

sys.path.append('G:\StockAnalysis_API\StockAnalysis-RealTime')

warnings.simplefilter(action='ignore', category=FutureWarning)

class StockMetadataIngestion:
    def __init__(self, stock_file_path: os.PathLike, market_country: str):
        self.stock_file_path = stock_file_path
        self.market_country = market_country
        self.output_dir = "Output"
        self.final_df = pd.DataFrame()
        
    def generate_stock_list(self):
        nse_stock_list = get_stock_list(input_file_path=self.stock_file_path, 
                              market_country=self.market_country)
        """Fetches the stock list from the specified file path."""
        return nse_stock_list
    
    def generate_information_df(self, stock_name):
        """Fetches and processes data for a specific stock."""
        try:
            stock_info_fetcher = StockInfoFetcher(stock_name)
            data_all_info = stock_info_fetcher.filter_stock_info()
            
            if data_all_info.empty or data_all_info.isna().all(axis=None):
                logger.warning(f"No valid data found for {stock_name}.")
                return None

            stock_analyzer = StockFeatureEngineering(stock_info_fetcher.stock, data_all_info)
            result = stock_analyzer.StockFeatureEngine()
            logger.info(f"Result fetched & stored for {stock_name}.")
            return result
        except ValueError as ve:
            logger.error(f"ValueError: {ve} for stock {stock_name}")
            return None
        except Exception as e:
            logger.error(f"Error occurred while processing {stock_name}: {e}")
            return None

    def save_df_to_csv(self, data: pd.DataFrame):
        """Saves the final DataFrame to a CSV file and returns the full absolute file path."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        file_path = os.path.join(self.output_dir, "Stock_Meta_Data.csv")
        data.to_csv(file_path, index=False)
        
        # Convert to absolute path
        absolute_file_path = os.path.abspath(file_path)
        return absolute_file_path  # Return the absolute path

    
    def ingest_metadata_stock(self):
        """Main function to ingest metadata for all stocks in the list."""
        # Fetch the list of stock tickers
        stock_list = self.generate_stock_list()

        logger.info(f'Total no of Records for which fetching Stock Details are: {len(stock_list)}\n\n')
        logger_terminal.info(f'Total no of Records for which fetching Stock Details are: {len(stock_list)}')

        for item in tqdm(stock_list):
            main_df = self.generate_information_df(item)
            
            # Only concatenate if main_df is not None and contains valid data
            if main_df is None or not isinstance(main_df, pd.DataFrame):
                logger.warning(f'No valid data returned for {item}. Skipping this stock.\n\n')
                continue
            else:
                self.final_df = pd.concat([self.final_df, main_df], ignore_index=True)
                logger.info(f'All Details Fetched & stored for {item}\n')

        logger.info(f'Total records in the final sheet: {self.final_df.shape[0]}\n')
        logger_terminal.info(f'Total records in the final sheet: {self.final_df.shape[0]}')

        url_metadata = self.save_df_to_csv(self.final_df)

        logger.info(f'Stock Meta Data Generated. URL - {url_metadata}')
        logger_terminal.info(f'Stock Meta Data Generated. URL - {url_metadata}')
        
        return url_metadata  # Return the CSV path if needed
