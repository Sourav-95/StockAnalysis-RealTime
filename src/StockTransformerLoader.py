import os
import sys
import pandas as pd
import warnings
from tqdm import tqdm
from src.StockIngestion import StockFeatureEngineering, StockInfoFetcher
from src.stock_list import Stock_List
from src_comp.logger import logger, logger_terminal

warnings.simplefilter(action='ignore', category=FutureWarning)

class StockMetadataIngestion:
    def __init__(self, stock_file_path: os.PathLike, market_country: str):
        self.stock_file_path = stock_file_path
        self.market_country = market_country
        self.output_dir = "Output"
        self.final_df = pd.DataFrame()
        
    def generate_stock_list(self):
        
        if self.market_country == 'India':
            nse_stock_list = Stock_List.get_stock_list_india(input_file_path=self.stock_file_path)
            return nse_stock_list
        elif self.market_country == 'USA':
            us_stock_list = Stock_List.get_stock_list_usa(input_file_path=self.stock_file_path)
            return us_stock_list
        else:
            logger_terminal.warning(f'Incorrect entry of Market Country. Enter Country Correctly. (Eg: India, USA...)')
    
    def generate_information_df(self, stock_name):

        """Fetches and processes data for a specific stock."""
        try:
            stock_info_fetcher = StockInfoFetcher(stock_name)
            data_all_info = stock_info_fetcher.filter_stock_info()
            
            if data_all_info.empty or data_all_info.isna().all(axis=None):
                logger.warning(f"No valid data found for {stock_name}.")
                return None
            else:
                stock_analyzer = StockFeatureEngineering(stock_info_fetcher.stock, 
                                                         data_all_info, 
                                                         market_country=self.market_country
                                                         )
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
        
        # Create specific file name o each country
        file_path = os.path.join(self.output_dir, f"Stock_Meta_Data_{self.market_country}.csv")
        data.to_csv(file_path, index=False)
        
        # Convert to absolute path
        absolute_file_path = os.path.abspath(file_path)
        return absolute_file_path  # Return the absolute path

    
    def ingest_metadata_stock(self):
        """Main function to ingest metadata for all stocks in the list."""

        # Fetch the list of stock tickers
        try:
            stock_list = self.generate_stock_list()
            logger.info(f'Total no of Records for which fetching Stock Details are: {len(stock_list)}\n\n')
            logger_terminal.info(f'Total no of Records for which fetching Stock Details are: {len(stock_list)}')
        except Exception as e:
            logger_terminal.warning(f'Error occurred in generate_stock_list() function: {e}')

        # Initialize an empty dataframe to store the results
        if stock_list:
            for item in tqdm(stock_list):
                main_df = None

                # Apply the logic only for India
                if self.market_country == "India":
                    main_df = self.generate_information_df(item)
                    if main_df is None or not isinstance(main_df, pd.DataFrame):
                        logger.warning(f'No valid data returned for {item}. Retrying with BSE ticker.')
                        item_bse = item.replace('.NS', '.BO') 
                        main_df = self.generate_information_df(item_bse)  
                        
                        if main_df is None or not isinstance(main_df, pd.DataFrame):
                            logger.warning(f'Still no valid data returned for {item_bse}. Skipping this stock.')
                            continue

                else:
                    main_df = self.generate_information_df(item)
                    if main_df is None or not isinstance(main_df, pd.DataFrame):
                        logger.warning(f'No valid data returned for {item}. Skipping this stock.')
                        continue

                # Concatenate valid data to the final DataFrame
                self.final_df = pd.concat([self.final_df, main_df], ignore_index=True)
                logger.info(f'All Details Fetched & stored for {item}\n')

            logger.info(f'Total records in the final DataFrame: {self.final_df.shape[0]}')
            logger_terminal.info(f'Total records in the final DataFrame: {self.final_df.shape[0]}')

            # Save the final DataFrame to CSV
            url_metadata = self.save_df_to_csv(self.final_df)

            logger.info(f'Stock Meta Data Generated. URL - {url_metadata}\n')
            logger_terminal.info(f'Stock Meta Data Generated. URL - {url_metadata}\n')

            return url_metadata  # Return the CSV path if needed
