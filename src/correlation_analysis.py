import pandas as pd
import os
import matplotlib.pyplot as plt
from textblob import TextBlob
import seaborn as sns

class CorrelationAnalyzer:
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
    def load_data(self, file_path):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        return self.data    
    def merge_csv_files(self, folder_path):
        """
        Merges all CSV files from the specified folder into one DataFrame and adds a 'stock_symbol' column.
        
        folder_path: str - Path to the folder containing CSV files.
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
    def calculate_daily_returns(self,price):
        daily_returns = price.pct_change()
        return daily_returns
    
    def correlation_matrix(self,data=None):
         # Use provided data or fall back to the internal DataFrame
        if data is None:
            data = self.data
        # Compute the correlation matrix
        self.data.drop(columns=['Stock Splits','Dividends'], axis=1, inplace=True)        
        corr_matrix = self.data.select_dtypes(include=['int', 'float']).corr()

        # Plot correlation using heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, cmap='coolwarm', annot=True,fmt=".2f", cbar=True, linewidths=0.5)
        plt.show()
    def correlation_each_symbol(self, data=None):
        # Use provided data or fall back to the internal DataFrame
        if data is None:
            data = self.data

        # Get unique stock symbols
        unique_symbols = data['Ticker_symbol'].unique()
        # Initialize a list to store correlation results
        correlation_results = []

        # Loop through each unique stock symbol
        for symbol in unique_symbols:
            # Filter data for the current symbol
            symbol_data = data[data['Ticker_symbol'] == symbol]
            
            # Calculate the correlation between 'polarity' and 'daily_return'
            correlation = symbol_data[['polarity', 'daily_return']].corr().loc['polarity', 'daily_return']
            
            # Append the result to the list
            correlation_results.append({'Ticker_symbol': symbol, 'correlation': correlation})

        # Convert the results list to a DataFrame
        correlation_df = pd.DataFrame(correlation_results)

        # Return the correlation DataFrame
        return correlation_df
    def visualize_relationships(self,aggregated_data=None):
        """
        Visualizes scatter plots to show relationships between Polarity and other financial metrics:
        Daily Return, Close Price, and Volume.
        
        Parameters:
            aggregated_data (DataFrame): Pandas DataFrame containing 'polarity', 'daily_return', 'Close', and 'Volume'.
        """
        # Set up the figure size
        plt.figure(figsize=(14, 10))
        
        # Scatter plot for Polarity vs. Daily Return
        plt.subplot(2, 2, 1)
        sns.scatterplot(x='polarity', y='daily_return', data=aggregated_data)
        plt.title('Polarity vs. Daily Return')
        plt.xlabel('Polarity')
        plt.ylabel('Daily Return')

        # Scatter plot for Polarity vs. Close Price
        plt.subplot(2, 2, 2)
        sns.scatterplot(x='polarity', y='Close', data=aggregated_data)
        plt.title('Polarity vs. Close Price')
        plt.xlabel('Polarity')
        plt.ylabel('Close Price')

        # Scatter plot for Polarity vs. Volume
        plt.subplot(2, 2, 3)
        sns.scatterplot(x='polarity', y='Volume', data=aggregated_data)
        plt.title('Polarity vs. Volume')
        plt.xlabel('Polarity')
        plt.ylabel('Volume')

        # Adjust layout and display the plots
        plt.tight_layout()
        plt.show()
    