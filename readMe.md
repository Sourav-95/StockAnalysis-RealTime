# STOCK META DATA 
### This is a script which will do complete ETL of listed Stock on Exchange from Yahoo Finance API
#### Development in Progress.
.
Input: 
1. List of Stock listed (Eg on NSE). Ticker Names can be downloaded or checked on official website.
2. Listed Website country (Eg. India, Others)  -  Currently only Build for India, rest Development in Progress

Output:
Condition 1: If input stock_name is correct and listed on NSE .. (Currently working on BSE)
            Then MetaData is Extracted from 
            Yahoo Finance --> Transformed(Feature Engineered) --> Loaded to a DataFrame and then converted to CSV as output.
Condition 2: If input stock_name is incorrect 
            404 ClientError and that particular record is skipped