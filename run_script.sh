#!/bin/bash

# Set the Python path (optional, if needed)
export PYTHONPATH="G:/StockAnalysis_API/StockAnalysis-RealTime"

# Activate your virtual environment
source G:/StockAnalysis_API/StockAnalysis-RealTime/myvenv/Scripts/activate

# Install dependencies from requirements.txt
# pip install -r G:/StockAnalysis_API/StockAnalysis-RealTime/requirements.txt

# Run your Python main script
python G:/StockAnalysis_API/StockAnalysis-RealTime/main.py

# Deactivate the virtual environment (optional)
deactivate
