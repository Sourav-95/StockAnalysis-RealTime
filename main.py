from src.StockTransformerLoader import StockMetadataIngestion
from components.logger import logger_terminal
from components.logger import logger
import time
import os

if __name__ == "__main__":
    try:
        # Define path for each country
        COUNTRY_FILE_MAP = {
            "India": os.path.join(os.getcwd(), 'inputs', 'stock_list_test.csv'),
            "USA": os.path.join(os.getcwd(), 'inputs', 'stock_list_test_usa.csv')
            # Add more countries while developing
        }

        start_time = time.time()

        for country, file_path in COUNTRY_FILE_MAP.items():
            logger.info(f'Starting ETL Process for :  {country}')
            logger_terminal.info(f'Starting ETL Process for : {country} ')

            # Create an instance of StockMetadataIngestion with Country Specific
            stock_ingestor = StockMetadataIngestion(stock_file_path=file_path, 
                                                    market_country=country
                                                    )
            
            stock_meta_data = stock_ingestor.ingest_metadata_stock()
        logger_terminal.info(f'Time taken for ETL process: -  {(time.time() - start_time).__round__(2)} seconds')
    except FileNotFoundError as e:
        logger_terminal.info(f'Error occured as : {e}')