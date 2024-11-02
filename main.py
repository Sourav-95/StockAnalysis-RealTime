from src.StockLoader import StockMetadataIngestion
from src_comp.logger import logger_terminal
import time

if __name__ == "__main__":
    try:
        stock_file_path = input("Enter the path to the stock list CSV file: ")
        market_country = input("Enter the market country (e.g., 'India' or 'Others'): ")

        # Create an instance of StockMetadataIngestion with user inputs
        start_time = time.time()
        stock_ingestor = StockMetadataIngestion(stock_file_path=stock_file_path, 
                                                market_country=market_country
                                                )
        
        stock_ingestor.ingest_metadata_stock()
        logger_terminal.info(f'Time taken for ETL process: -  {(time.time() - start_time).__round__(2)} seconds')
    except FileNotFoundError as e:
        logger_terminal.info(f'Error occured as : {e}')