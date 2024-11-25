from src.StockTransformerLoader import StockMetadataIngestion
from src.StockIngestion import StockInfoFetcher
from components.logger import logger_terminal
import pandas as pd
from tqdm import tqdm

stock_file_path = r'G:\StockAnalysis_API\inputs\stock_list.csv'
market_country = "India"

stock_loader = StockMetadataIngestion(stock_file_path=stock_file_path, 
                                                market_country=market_country
                                                )
# stock_ingestor.ingest_metadata_stock()/
# result = stock_loader.generate_information_df(stock_name='MPHASIS.NS')
# result.to_csv('test_output.csv', index=False)

def ingest_metadata_stock():
    """Main function to ingest metadata for all stocks in the list."""
    
    # Fetch the list of stock tickers
    stock_list_nse = ['MPHASIS.NS', 'BSOFT.NS', 'WAAREERTL.NS']
    final_df = pd.DataFrame()
    logger_terminal.info(f'Total no of Records for which fetching Stock Details are: {len(stock_list_nse)}')
    
    for item in stock_list_nse:
        # Attempt to fetch data for NSE ticker
        main_df = stock_loader.generate_information_df(item)
        
        # If no data is returned, retry with BSE ticker
        if main_df is None or not isinstance(main_df, pd.DataFrame):
            logger_terminal.warning(f'No valid data returned for {item}. Retrying with BSE ticker.')
            item_bse = item.replace('.NS', '.BO')
            main_df = stock_loader.generate_information_df(item_bse)
            
            if main_df is None or not isinstance(main_df, pd.DataFrame):
                logger_terminal.warning(f'Still no valid data returned for {item_bse}. Skipping this stock.')
                continue  # Skip to the next stock if no data is available
        
        # Concatenate valid data to the final DataFrame
        final_df = pd.concat([final_df, main_df], ignore_index=True)
        logger_terminal.info(f'All Details Fetched & stored for {item}')

    # Check if any data was retrieved before saving
    if final_df.empty:
        logger_terminal.warning("No data was fetched for any stocks.")
        return None  # Or handle as needed

    # Save final DataFrame and log the URL
    logger_terminal.info(f'Total records in the final sheet: {final_df.shape[0]}')
    url_metadata = stock_loader.save_df_to_csv(final_df)
    logger_terminal.info(f'Stock Meta Data Generated. URL - {url_metadata}')
    
    return url_metadata  # Return the CSV path if needed
ingest_metadata_stock()