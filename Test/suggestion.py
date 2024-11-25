import pandas as pd
import yfinance as yf
from components.logger import logger

class StockInfoFetcher:
    """Class to fetch and filter stock information from Yahoo Finance."""

    info_keys = [
        'symbol', 'shortName', 'industry', 'sector', 'longBusinessSummary', 'financialCurrency', 'marketCap',
        'previousClose', 'currentPrice', 'targetHighPrice', 'targetLowPrice', 'targetMeanPrice', 'targetMedianPrice',
        'volume', 'averageVolume10days', 'dividendRate', 'dividendYield', 'exDividendDate', 'trailingAnnualDividendRate',
        'trailingAnnualDividendYield', 'payoutRatio', 'fiveYearAvgDividendYield', 'beta', 'trailingPE', 'forwardPE',
        'enterpriseValue', 'fiftyTwoWeekLow', 'fiftyTwoWeekHigh', 'priceToSalesTrailing12Months', 'twoHundredDayAverage',
        'profitMargins', 'bookValue', 'priceToBook', 'trailingEps', 'forwardEps', 'enterpriseToRevenue', 'enterpriseToEbitda',
        'firstTradeDateEpochUtc', 'recommendationKey', 'numberOfAnalystOpinions', 'totalCash', 'totalCashPerShare',
        'ebitda', 'totalDebt', 'quickRatio', 'currentRatio', 'totalRevenue', 'debtToEquity', 'revenuePerShare',
        'returnOnAssets', 'returnOnEquity', 'freeCashflow', 'operatingCashflow', 'earningsGrowth', 'revenueGrowth',
        'grossMargins', 'ebitdaMargins', 'operatingMargins', 'trailingPegRatio', 'netIncomeToCommon'
    ]

    def __init__(self, stock_name):
        self.stock_name = stock_name
        self.stock = yf.Ticker(stock_name)

    def get_stock_info(self):
        """Fetches stock information from Yahoo Finance."""
        try:
            all_info = self.stock.info
            logger.info(f"Successfully fetched stock info for {self.stock_name}.")
            return all_info
        except Exception as e:
            logger.error(f"Error fetching stock info for {self.stock_name}: {e}")
            return {}

    def filter_stock_info(self):
        """Filters specific stock attributes based on predefined keys."""
        all_info = self.get_stock_info()
        try:
            filtered_info = {key: all_info[key] for key in self.info_keys if key in all_info}
            logger.info("Filtered stock information successfully.")
            return pd.DataFrame([filtered_info])
        except Exception as e:
            logger.error(f"Error filtering stock info: {e}")
            return pd.DataFrame()


class StockAnalyzer:
    """Class to analyze stock metrics and calculate growth rates."""

    def __init__(self, stock, data_all_info):
        self.stock = stock
        self.data_all_info = data_all_info

    def find_growth(self, attribute):
        """Calculates 1-year and 5-year growth for a specified attribute."""
        try:
            data = self.stock.financials
            _1Y_growth = (data.iloc[:, 0].loc[attribute] - data.iloc[:, 1].loc[attribute]) / data.iloc[:, 1].loc[attribute]
            _5Y_growth = (data.iloc[:, 0].loc[attribute] - data.iloc[:, 3].loc[attribute]) / data.iloc[:, 3].loc[attribute] / 3
            logger.info(f"Calculated growth for {attribute}: 1Y {_1Y_growth}, 5Y {_5Y_growth}.")
            return _1Y_growth, _5Y_growth
        except Exception as e:
            logger.error(f"Error calculating growth for {attribute}: {e}")
            return None, None

    def add_growth_features(self):
        """Adds growth features for EBITDA, Total Revenue, Net Income, and Pretax Income."""
        try:
            # Calculating growth for various attributes
            growth_features = {
                '1Y EBITDA Growth': self.find_growth('EBITDA')[0],
                '5Y EBITDA Growth': self.find_growth('EBITDA')[1],
                '1Y Total Revenue Growth': self.find_growth('Total Revenue')[0],
                '5Y Total Revenue Growth': self.find_growth('Total Revenue')[1],
                '1Y Net Income Growth': self.find_growth('Net Income')[0],
                '5Y Net Income Growth': self.find_growth('Net Income')[1],
                '1Y PreTax Income Growth': self.find_growth('Pretax Income')[0],
                '5Y PreTax Income Growth': self.find_growth('Pretax Income')[1],
            }
            for key, value in growth_features.items():
                self.data_all_info[key] = value
            logger.info("Added growth features to the DataFrame.")
        except Exception as e:
            logger.error(f"Error adding growth features: {e}")

    def calculate_additional_metrics(self):
        """Calculates additional metrics for the stock data."""
        try:
            self.data_all_info['netIncomeMargin'] = self.data_all_info['netIncomeToCommon'] / self.data_all_info['totalRevenue']
            self.data_all_info['% Away From 52High'] = (self.data_all_info['fiftyTwoWeekHigh'] / self.data_all_info['currentPrice']) - 1
            self.data_all_info['% Away From 52Low'] = (self.data_all_info['currentPrice'] / self.data_all_info['fiftyTwoWeekLow']) - 1
            logger.info("Calculated additional metrics.")
        except Exception as e:
            logger.error(f"Error calculating additional metrics: {e}")

    def analyze(self):
        """Runs the analysis process and returns the final DataFrame."""
        self.add_growth_features()
        self.calculate_additional_metrics()
        logger.info("Completed stock analysis.")
        return self.data_all_info


def main(stock_name):
    """Main function to execute the stock fetching and analysis."""
    stock_info_fetcher = StockInfoFetcher(stock_name)
    data_all_info = stock_info_fetcher.filter_stock_info()

    stock_analyzer = StockAnalyzer(stock_info_fetcher.stock, data_all_info)
    result = stock_analyzer.analyze()

    logger.info("Final DataFrame:\n" + str(result))
    return result


# Run the main function and log output
if __name__ == "__main__":
    stock_name = "RELIANCE.NS"
    main(stock_name)
