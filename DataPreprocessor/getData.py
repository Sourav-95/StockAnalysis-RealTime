import pandas as pd
import numpy as np
import yfinance as yf

stock_name = "RELIANCE.NS"
stock_ = yf.Ticker(stock_name)

# get all stock info
all_info = stock_.info

# List of keys to filter
info_keys = ['symbol', 'shortName', 'industry', 'sector', 'longBusinessSummary','financialCurrency','marketCap', 'previousClose',
             'currentPrice', 'targetHighPrice', 'targetLowPrice', 'targetMeanPrice', 'targetMedianPrice', 'volume', 'averageVolume10days',
             'dividendRate', 'dividendYield', 'exDividendDate', 'trailingAnnualDividendRate', 'trailingAnnualDividendYield',
             'payoutRatio', 'fiveYearAvgDividendYield','beta', 'trailingPE', 'forwardPE',
             'enterpriseValue', 'fiftyTwoWeekLow', 'fiftyTwoWeekHigh', 'priceToSalesTrailing12Months', 'twoHundredDayAverage',
             'profitMargins',  'bookValue', 'priceToBook', 'trailingEps', 'forwardEps','enterpriseToRevenue', 'enterpriseToEbitda',
             'firstTradeDateEpochUtc', 'recommendationKey', 'numberOfAnalystOpinions', 'totalCash', 'totalCashPerShare',
             'ebitda', 'totalDebt', 'quickRatio', 'currentRatio', 'totalRevenue', 'debtToEquity',
             'revenuePerShare', 'returnOnAssets', 'returnOnEquity', 'freeCashflow', 'operatingCashflow',
             'earningsGrowth', 'revenueGrowth', 'grossMargins', 'ebitdaMargins', 'operatingMargins','trailingPegRatio', 'netIncomeToCommon']


# Filter the dictionary
filtered_all_info = {key: all_info[key] for key in info_keys if key in all_info}

#converting to DataFrame
data_all_info = pd.DataFrame([filtered_all_info])

# function to get 1Y and 5Y Growth Strategy
def find_growth(attribute:str):
  data = stock_.income_stmt
  _1Y_growth = (data.iloc[:,0].loc[attribute] - data.iloc[:,1].loc[attribute])/data.iloc[:,1].loc[attribute]
  _5Y_growth = (data.iloc[:,0].loc[attribute] - data.iloc[:,3].loc[attribute])/data.iloc[:,3].loc[attribute]
  _5Y_growth = _5Y_growth/3
  return _1Y_growth, _5Y_growth

# Feature Engineering 
_1Y_EBITDA_Growth, _5Y_EBITDA_Growth = find_growth(attribute='EBITDA')
_1Y_TotalRevenue_Growth, _5Y_TotalRevenue_Growth = find_growth(attribute='Total Revenue')
_1Y_TotalIncome_Growth, _5Y_TotalIncome_Growth = find_growth(attribute='Net Income')
_1Y_PreTaxIncome_Growth, _5Y_PreTaxIncome_Growth = find_growth(attribute='Pretax Income')

# Adding Features
data_all_info['netIncomeMargin'] = data_all_info['netIncomeToCommon']/data_all_info['totalRevenue']
data_all_info['% Away From 52High'] = (data_all_info['fiftyTwoWeekHigh']/data_all_info['currentPrice'])-1
data_all_info['% Away From 52Low'] = (data_all_info['currentPrice']/data_all_info['fiftyTwoWeekLow'])-1

data_all_info['1Y Total Revenue Growth'] = _1Y_TotalRevenue_Growth
data_all_info['5Y Total Revenue Growth'] = _5Y_TotalRevenue_Growth

data_all_info['1Y EBITDA Growth'] = _1Y_EBITDA_Growth
data_all_info['5Y EBITDA Growth'] = _5Y_EBITDA_Growth


data_all_info['1Y PreTax Income Growth'] = _1Y_PreTaxIncome_Growth
data_all_info['5Y PreTax Income Growth'] = _5Y_PreTaxIncome_Growth

data_all_info['1Y Net Income Growth'] = _1Y_TotalIncome_Growth
data_all_info['5Y Net Income Growth'] = _5Y_TotalIncome_Growth

data_all_info.to_csv('output_.csv')