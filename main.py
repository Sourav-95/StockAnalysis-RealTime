from src.StockLoader import StockMetadataIngestion

if __name__ == "__main__":

    stock_file_path = input("Enter the path to the stock list CSV file: ")
    market_country = input("Enter the market country (e.g., 'India' or 'Others'): ")
    
    # Create an instance of StockMetadataIngestion with user inputs
    stock_ingestor = StockMetadataIngestion(stock_file_path=stock_file_path, 
                                            market_country=market_country
                                            )
    
    stock_ingestor.ingest_metadata_stock()