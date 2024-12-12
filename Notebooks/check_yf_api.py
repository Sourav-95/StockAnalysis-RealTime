from src.StockIngestion import StockInfoFetcher

stock_name = 'WAAREERTL.BO'

stock_info_fetcher = StockInfoFetcher(stock_name)
data_all_info = stock_info_fetcher.ingest_and_filter_stock_info()

print(data_all_info)

