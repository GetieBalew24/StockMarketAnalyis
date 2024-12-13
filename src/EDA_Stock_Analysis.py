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
    
    def plot_article_per_publisher(self):
        publisherCounts = self.article_per_publisher().nlargest(5, 'Article Count')
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Publisher', y='Article Count', data=publisherCounts)
        plt.xticks(rotation=90)
        plt.xlabel('Publisher')
        plt.ylabel('Number of Articles')
        plt.title('Number of Articles for each Publisher')
        plt.show()
    
    def analyze_publication_dates(self):
        """Analyze publication dates to identify trends over time."""
        self.data['date'] = pd.to_datetime(self.data['date'], errors='coerce',utc=True)
        self.data['year'] = self.data['date'].dt.year
        self.data['month'] = self.data['date'].dt.month
        self.data['day_of_week'] = self.data['date'].dt.day_name()

        # Articles over time by year and month
        articlesOverTime = self.data.groupby(['year', 'month']).size().reset_index(name='article_count')

        # Articles by day of the week
        articlesByDay = self.data['day_of_week'].value_counts()

        return articlesOverTime, articlesByDay
    
    def plot_article_trends(self, articles_over_time, articles_by_day):
        """Plot trends of article counts over time and by day of the week."""
        # Plotting article counts over time
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=articles_over_time, x='month', y='article_count', hue='year', marker='o')
        plt.title('Article Count Time')
        plt.xlabel('Month')
        plt.ylabel('Number of Articles')
        plt.show()

        # Plotting article counts by day of the week
        plt.figure(figsize=(10, 5))
        sns.barplot(x=articles_by_day.index, y=articles_by_day.values)
        plt.title('Article Count by Day of the Week')
        plt.xlabel('Day of the Week')
        plt.ylabel('Number of Articles')
        plt.show()

    # Text Analyis
    def text_preprocess(self):
        # Convert to lowercase and remove non-alphabetic characters
        self.data['cleaned_headline']=self.data['headline'].str.lower().str.replace(r'[^a-zA-Z\s]', '', regex=True) 
        # Remove leading and trailing whitespace
        self.data['cleaned_headline']=self.data['cleaned_headline'].str.strip() 
        # remove stop words
        stop_words = set(stopwords.words('english'))
        self.data['cleaned_headline'] = self.data['cleaned_headline'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
        return self.data
    