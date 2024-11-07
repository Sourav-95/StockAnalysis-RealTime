import pandas as pd
import yfinance as yf
from requests.exceptions import HTTPError
from src_comp.logger import logger
from src.FeatureInfo import feature_attribute

class StockInfoFetcher:
    """Class to fetch and filter stock information from Yahoo Finance."""

    # Get all the Described Feature from the list
    all_features = feature_attribute()

    def __init__(self, stock_name):
        self.stock_name = stock_name
        self.stock = yf.Ticker(stock_name)
    
    def get_stock_info(self):
        # Fetches Stock information from Yahoo Finance
        try:
            ### Calling from Yahoo Finance API ###
            all_info = self.stock.info
            logger.info(f'Fetching stock inforation completed for {self.stock_name}.')
            return all_info
        except HTTPError as e:
            if e.response.status_code == 404:
                return 'Client  Error'
            else:
                raise
        except Exception as e:
            return f'error: {str(e)}'
        
    def filter_stock_info(self):
        # Filters specific stock attributes based on predefined keys
        all_info = self.get_stock_info()
        if all_info:
            try:
                filtered_info = {key: all_info[key] for key in self.all_features if key in all_info}
                logger.info(f"Filtered stock information successfully for {self.stock_name}")
                return pd.DataFrame([filtered_info])
            except Exception as e:
                logger.debug(f"Error filtering stock info for {self.stock_name} as : {e}")
                return pd.DataFrame()

class StockFeatureEngineering():
    """Class to analyze the stock metrics and calculate growth rates"""

    def __init__(self, stock, data_all_info):
        self.stock = stock
        self.data_all_info = data_all_info

    def find_growth_income(self, attribute):
        # Calculates 1-Year and 5-Year growth for a specified attribute
        try:
            ### Calling from Yahoo Finance API (.cash_flow) ###
            data = self.stock.income_stmt
            _1Y_growth = (data.iloc[:, 0].loc[attribute] - data.iloc[:, 1].loc[attribute]) / data.iloc[:, 1].loc[attribute]
            _5Y_growth = (data.iloc[:, 0].loc[attribute] - data.iloc[:, 3].loc[attribute]) / data.iloc[:, 3].loc[attribute] / 3
            logger.info(f"Calculated growth for {attribute}: 1Y & 5Y.")
            return _1Y_growth, _5Y_growth
        except Exception as e:
            logger.debug(f"Error calculating growth for {attribute}: {e}")
            return None, None
        
    def find_growth_cashflow(self, attribute):
        # Calculates 1-Year and 5-Year growth for a specified attribute
        try:
            ### Calling from Yahoo Finance API (.cash_flow) ###
            data = self.stock.cash_flow                     
            cash_flow_attribute = data.iloc[:, 0].loc[attribute]
            logger.info(f"Fetched {attribute} for last Year")
            return cash_flow_attribute
        except Exception as e:
            logger.debug(f"Error calculating growth for {attribute}: {e}")
            return None, None
    
    def add_growth_features(self):
        # Adds growth features for EBITDA, Total Revenue, Net Income, and Pretax Income.
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
            logger.debug(f"Error adding growth features: {e}")

    def calculate_additional_metrics(self):
        # Calculates additional metrics for the stock data
        try:
            self.data_all_info['netIncomeMargin'] = self.data_all_info['netIncomeToCommon'] / self.data_all_info['totalRevenue']
            self.data_all_info['% Away From 52High'] = (self.data_all_info['fiftyTwoWeekHigh'] / self.data_all_info['currentPrice']) - 1
            self.data_all_info['% Away From 52Low'] = (self.data_all_info['currentPrice'] / self.data_all_info['fiftyTwoWeekLow']) - 1
            logger.info("Calculated additional metrics.")
        except Exception as e:
            logger.debug(f"Error calculating additional metrics: {e}")

    def convert_market_cap_to_cr(self):
        """Converts marketCap from absolute terms to crores."""
        try:
            self.data_all_info['MarketCap_Crores'] = self.data_all_info['marketCap'] / 10000000  # Divide by 10 million
            logger.info("Converted marketCap to crores.")
        except Exception as e:
            logger.debug(f"Error converting marketCap to crores: {e}")

    def add_market_category(self):
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
            logger.debug(f"Error adding market category: {e}")

    def StockFeatureEngine(self):
        # Runs the analysis process and returns the final DataFrame
        self.add_growth_features()
        self.calculate_additional_metrics()
        self.convert_market_cap_to_cr()
        self.add_market_category()
        logger.info("Feature Engineering Completed")
        return self.data_all_info
