import sys
import pandas as pd
import yfinance as yf
from DataPreprocessor.get_scrapper import StockScrapper
from components.logger import logger
from src.FeatureInfo import feature_attribute
from components.exception import CustomException
from components.exception import log_and_raise_exception

class StockInfoFetcher:
    """
    This Class to used to fetch stock information & filter the requried 
    Information as per feature_attributes().
    
    Args:
        stock_name(str) : The Name of the Stock to fetch information using its Exchange (Eg: RELIANCE.NS)
    
    Function:
        1. Initialize the yfinance.Ticker(stock_name)
        2. gets_info_dict() --> from class StockScrapper
        3. filters the return from get_info_dict()

    Returns:
        Dataframe
    """

    # Get all the Described Feature from the list
    all_features = feature_attribute()

    def __init__(self, stock_name):
        self.stock_name = stock_name
        self.stock = yf.Ticker(stock_name)
    
    # StockScrapper Module which request API from Yahoo Finance
    def get_stock_info(self):

        
        info_dict = StockScrapper(ticker_base=self.stock)._scrapper_()
        logger.info(f'Fetching stock inforation completed for {self.stock_name}.')
        return info_dict
            
    # Filters specific stock attributes based on predefined keys   
    def ingest_and_filter_stock_info(self):
        
        all_info = self.get_stock_info()
        if all_info:
            filtered_info = {key: all_info[key] for key in self.all_features if key in all_info}
            logger.info(f"Filtered stock information successfully for {self.stock_name}")
            return pd.DataFrame([filtered_info])

class StockFeatureEngineering():
    """
    This Class to used to ingest additional data from Yahoo Finance API & 
    analyze the stock metrics and calculate growth rates
    
    Args: 
        stock (yf.Ticker.stock_name) : This is the class object instance which is invoked from StockInfoFetcher(stock_name)
        data_all_info (DataFrame) : This is a dictionary argument from StockInfoFetcher result
        market_country (str) : String Value used for certain FeatureEngginering

    Returns:
        data_all_info (DataFrame) : After Feature Engineering according to the Certain Condition
    """

    def __init__(self, stock, data_all_info, market_country):
        self.stock = stock
        self.data_all_info = data_all_info
        self.market_country = market_country

    # Calculates 1-Year and 5-Year growth for a specified attribute after ingesting data from Yahoo Finance API
    def find_growth_income(self, attribute):
        
        try:
            data = self.stock.income_stmt                   # .income_stmt is API call to get Financial income statement data
            
            if len(data)>0:
                if attribute in data.index: 
                    _1Y_growth = (data.iloc[:, 0].loc[attribute] - data.iloc[:, 1].loc[attribute]) / data.iloc[:, 1].loc[attribute]
                    _5Y_growth = (data.iloc[:, 0].loc[attribute] - data.iloc[:, 3].loc[attribute]) / data.iloc[:, 3].loc[attribute] / 3
                    logger.info(f"Calculated growth for {attribute}: 1Y & 5Y.")
                else:
                    _1Y_growth = None 
                    _5Y_growth = None
            else:
                _1Y_growth = None
                _5Y_growth = None
                logger.info(f"Data Source doesn't have valid data for {attribute}")
            return _1Y_growth, _5Y_growth
        except IndexError as e:
            log_and_raise_exception(e,sys, f"Failed to Calculate growth for {attribute} for Index Error")
            return None, None
        except Exception as e:
            log_and_raise_exception(e,sys, f"Failed to Calculate growth for {attribute}")
            return None, None

    # Calculates 1-Year and 5-Year CashFlow growth for a specified attribute after ingesting data from Yahoo Finance API   
    def find_growth_cashflow(self, attribute):
        try:
            data = self.stock.cash_flow 

            if len(data)>0: 
                if attribute in data.index:
                    cash_flow_attribute = data.iloc[:, 0].loc[attribute]
                    logger.info(f"Calculated growth for  {attribute} for last Year")
                else:
                    cash_flow_attribute = None
            else:
                logger.info(f"Data Source doesn't have valid data for {attribute}")
                cash_flow_attribute = None
            return cash_flow_attribute
        except IndexError as e:
            log_and_raise_exception(e,sys, f"Failed to Calculate growth of cashflow for {attribute} for Index Error")
            return None
        except Exception as e:
            log_and_raise_exception(e,sys, f"Failed to calculate growth of CashFlow")
            return None
    
    # Adds growth features for EBITDA, Total Revenue, Net Income, and Pretax Income.
    def add_growth_features(self):
        
        try:
            growth_features = {
                '1Y EBITDA Growth': self.find_growth_income('EBITDA')[0],
                '5Y EBITDA Growth': self.find_growth_income('EBITDA')[1],
                '1Y Total Revenue Growth': self.find_growth_income('Total Revenue')[0],
                '5Y Total Revenue Growth': self.find_growth_income('Total Revenue')[1],
                '1Y Net Income Growth': self.find_growth_income('Net Income')[0],
                '5Y Net Income Growth': self.find_growth_income('Net Income')[1],
                '1Y PreTax Income Growth': self.find_growth_income('Pretax Income')[0],
                '5Y PreTax Income Growth': self.find_growth_income('Pretax Income')[1],
                'FinancingCashFlow Activity': self.find_growth_cashflow('Financing Cash Flow'),
                'InvestingCashFlow Activity': self.find_growth_cashflow('Investing Cash Flow'),
                'OperatingCashFlow Activity': self.find_growth_cashflow('Operating Cash Flow'),
            }
            for key, value in growth_features.items():
                self.data_all_info[key] = value
            logger.info("Added growth features to the DataFrame.")
        except Exception as e:
            log_and_raise_exception(e,sys, "Failed in adding Growth Features")

    # Calculates additional metrics for the stock data
    def calculate_additional_metrics(self):
        try:
            self.data_all_info['netIncomeMargin'] = self.data_all_info['netIncomeToCommon'] / self.data_all_info['totalRevenue']
            self.data_all_info['% Away From 52High'] = (self.data_all_info['fiftyTwoWeekHigh'] / self.data_all_info['currentPrice']) - 1
            self.data_all_info['% Away From 52Low'] = (self.data_all_info['currentPrice'] / self.data_all_info['fiftyTwoWeekLow']) - 1
            logger.info("Calculated additional metrics.")
        except Exception as e:
            log_and_raise_exception(e,sys, "Failed in calculating additional metrics")

    def convert_market_cap_to_cr(self):
        """Converts marketCap from absolute terms to crores."""
        try:
            if self.market_country == 'India':
                self.data_all_info['MarketCap_Crores'] = self.data_all_info['marketCap'] / 10000000  # Divide by 10 million
                self.data_all_info.drop(columns=['marketCap'], axis=1, inplace=True)
                logger.info("Converted marketCap to crores.")
        except Exception as e:
            log_and_raise_exception(e,sys, "Failed to convert market cap")

    def add_ind_market_category(self):
        """Adds market category based on marketCap."""
        try:
            def categorize_market_cap(row):
                if row['MarketCap_Crores'] >= 96190.02:
                    return 'Large Cap'
                elif row['MarketCap_Crores'] >= 32592.19:
                    return 'Mid Cap'
                else:
                    return 'Small Cap'
            
            self.data_all_info['marketCategory'] = self.data_all_info.apply(categorize_market_cap, axis=1)
            logger.info("Added market category based on marketCap.")
        except Exception as e:
            log_and_raise_exception(e,sys, "Failed in adding Ind Market Category")
    
    # Runs the Main FeatureEngineering Functions / process and returns the final DataFrame
    def StockFeatureEngine(self):
        
        self.add_growth_features()
        self.calculate_additional_metrics()
        self.convert_market_cap_to_cr()
        if self.market_country == 'India':
            self.add_ind_market_category()
        logger.info("Feature Engineering Completed")
        return self.data_all_info