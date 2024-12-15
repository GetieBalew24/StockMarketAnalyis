import pandas as pd
import os
import pynance as pn
import talib
import matplotlib.pyplot as plt
import plotly.express as px

class StockPriceAnalyzer:
    def __init__(self, file_path=None, folder_path=None):
        """
        Initializes the StockPriceAnalyzer class with a CSV file path or a folder path.
        
        param file_path: str (optional) - Path to a single CSV file containing stock data.
        param folder_path: str (optional) - Path to a folder containing multiple CSV files to be merged.
        """
        self.file_path = file_path
        self.folder_path = folder_path
        self.data = pd.DataFrame()
        
        if self.file_path:
            # Load data from a single CSV file
            self.data = pd.read_csv(file_path)
        elif self.folder_path:
            # Automatically merge CSV files from the specified folder
            self.merge_csv_files(folder_path)

    #merge all stock csv files
    def merge_csv_files(self, folder_path):
        """
        Merges all CSV files from the specified folder into one DataFrame and adds a 'stock_symbol' column.
        
        param folder_path: str - Path to the folder containing CSV files.
        return: DataFrame - Merged DataFrame of all CSV files in the folder.
        """
        merged_df = pd.DataFrame()
        for file in os.listdir(folder_path):
            if file.endswith('.csv'):
                file_path = os.path.join(folder_path, file)
                df = pd.read_csv(file_path)
                
                # Extract stock symbol from the file name before the underscore
                stock_symbol = os.path.splitext(file)[0].split('_')[0]  # Extract symbol before the underscore
                
                # Add the stock_symbol column to the DataFrame
                df['stock_symbol'] = stock_symbol
                
                # Merge the DataFrame into the main DataFrame
                merged_df = pd.concat([merged_df, df], ignore_index=True)
        
        self.data = merged_df
        return self.data
    
         #Apply Analysis Indicators with TA-Lib 
    def calculate_technical_indicators(self, data):
        self.data['Data']=pd.to_datetime(self.data['Date'], format='ISO8601')
        # Calculate various technical indicators
        data['SMA'] = talib.SMA(data['Close'], timeperiod=20)
        data['RSI'] = talib.RSI(data['Close'], timeperiod=14)
        data['EMA'] = talib.EMA(data['Close'], timeperiod=20)
        macd, macd_signal, _ = talib.MACD(data['Close'])
        data['MACD'] = macd
        data['MACD_Signal'] = macd_signal
        return data
    
    # Stock Price with Moving Average
    def plot_stock_data(self, data, symbol):
        self.data['Date'] = pd.to_datetime(self.data['Date'],errors='coerce',utc=True)
        plt.figure(figsize=(10, 5))
        plt.plot(data['Date'], data['Close'], label='Close')
        plt.plot(data['Date'], data['SMA'], label='SMA')
        plt.title(f'{symbol} Stock Price with Moving Average')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()

    # Stock Price with Relative Strength Index (RSI)
    def plot_rsi(self, data, symbol):
        plt.figure(figsize=(10, 5))
        plt.plot(data['Date'], data['RSI'], label='RSI')
        plt.title(f'{symbol} Relative Strength Index (RSI)')
        plt.xlabel('Date')
        plt.ylabel('RSI')
        plt.legend()
        plt.show()
    
    # Stock Price with Exponential Moving Average
    def plot_ema(self, data, symbol):
        plt.figure(figsize=(10, 5))
        plt.plot(data['Date'], data['Close'], label='Close')
        plt.plot(data['Date'], data['EMA'], label='EMA')
        plt.title(f'{symbol} Stock Price with Exponential Moving Average')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()

    def visualize_stocks(self, stock_data):
        # Loop through each stock symbol
        self.data['Date'] = pd.to_datetime(self.data['Date'],errors='coerce',utc=True)
        for symbol in stock_data['stock_symbol'].unique():
            data = stock_data[stock_data['stock_symbol'] == symbol].copy()
            data = self.calculate_technical_indicators(data)
            
            # Plot all indicators for each stock symbol
            self.plot_stock_data(data, symbol)
            self.plot_rsi(data, symbol)
            self.plot_ema(data, symbol)


    
    