from src.StockTransformerLoader import StockMetadataIngestion
from src_comp.logger import logger_terminal
import time
import os

if __name__ == "__main__":
    try:
        STOCK_FILE_NAME = "stock_list_test.csv"
        INPUT_FILE_PATH = os.path.join(os.getcwd(), 'inputs', STOCK_FILE_NAME)
        COUNTRY = "India"

        # Create an instance of StockMetadataIngestion with user inputs
        start_time = time.time()
        stock_ingestor = StockMetadataIngestion(stock_file_path=INPUT_FILE_PATH, 
                                                market_country=COUNTRY
                                                )
        
        stock_ingestor.ingest_metadata_stock()
        logger_terminal.info(f'Time taken for ETL process: -  {(time.time() - start_time).__round__(2)} seconds')
    except FileNotFoundError as e:
        logger_terminal.info(f'Error occured as : {e}')