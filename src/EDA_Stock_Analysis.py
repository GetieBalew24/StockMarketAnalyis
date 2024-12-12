import re

import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import seaborn as sns
from nltk.corpus import stopwords
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer

class StockMarketAnalysis:
    def __init__(self, file_path):
        self.file_path = file_path
        # read .csv file
    def load_data(self):
        self.data = pd.read_csv(self.file_path)
        return self.data
        # check data quality
    def check_data_quality(self):
        # Check for missing values
        missing_values = self.data.isnull().sum()
        print("Missing values:")
        print(missing_values)

        # Check for duplicates
        duplicates = self.data.duplicated().sum()
        print("\n Number of duplicates:", duplicates)

        # Check data types
        data_types = self.data.dtypes
        print("\n Data types:")
        print(data_types)
    
     # Drops the 'Unnamed' column from a pandas DataFrame
    def drop_unnamed_column(self):
        
        self.data = self.data.drop(['Unnamed: 0'], axis=1)
        return self.data
    
        # Descriptive Statistics Analysis
    def headline_length_stats(self):
        
        self.data['headline_length'] = self.data['headline'].str.len()
        print("Headline Length Statistics:")
        return self.data['headline_length'].describe()
    
      # Number of Articles in each publisher 
    def article_per_publisher(self):
        publisherCounts = self.data['publisher'].value_counts().to_frame().reset_index()
        publisherCounts.columns = ['Publisher', 'Article Count']
        print("Article Counts per Publisher:")
        return publisherCounts