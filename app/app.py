import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.getcwd()))
# Import necessary functions from the eda.py script
from src.EDA_Stock_Analysis import *

# Load the data
file_path='../data/raw_analyst_ratings/raw_analyst_ratings.csv'
# create an object
text_analyser=StockMarketAnalysis(file_path)
text_analyser.load_data()

# Sidebar for navigation
st.sidebar.header("EDA Descriptive Statistics Report")
options = st.sidebar.selectbox("Select an EDA Descriptive Statistics Report", 
                               ["Headline length statistics", 
                                "Article Counts per Publisher", 
                                "Articles over time and by day",
                                "Article Trends", 
                                ])

# Display the selected analysis
if options == "Headline length statistics":
    st.subheader("Headline length statistics")
    summery=text_analyser.headline_length_stats()
    st.write(summery)
elif options == "Article Counts per Publisher":
    st.subheader("Article Counts per Publisher")
    articles_per_publisher=text_analyser.article_per_publisher()
    st.write(articles_per_publisher)
elif options == "Articles over time and by day":
    st.subheader("Articles over time and by day")
    articles_over_time, articles_by_day = text_analyser.analyze_publication_dates()
    st.write(articles_over_time)
    st.write(articles_by_day)
elif options == "Article Trends":
    st.subheader("Article Trends")
    articles_over_time, articles_by_day = text_analyser.analyze_publication_dates()
    st.pyplot(text_analyser.plot_article_trends(articles_over_time, articles_by_day))
else:
    st.write("please selecte the report")
    
# Sidebar for navigation
st.sidebar.header("Text Analysis(Sentiment analysis & Topic Modeling)")
option2 = st.sidebar.selectbox("Select Sentiment analysis Report", 
                               ["Plot Sentiment Distribution", 
                                "Word Frequency Distribution", 
                                ])

# Display the selected analysis
if option2 == "Plot Sentiment Distribution":
    st.subheader("Plot Sentiment Distribution")
    sent_dist=text_analyser.plot_sentiment_distribution()
    st.pyplot(sent_dist)
elif option2 == "Word Frequency Distribution":
    st.subheader("Word Frequency Distribution")
    word_freq=text_analyser.word_frequency()
    st.pyplot(word_freq)

# Sidebar for navigation
st.sidebar.header("Time Series Analysis")
option3 = st.sidebar.selectbox("Select Time Series analysis Report", 
                               ["Publication Frequency and publication Time", 
                                "Plot Time Series Trends", 
                                ])

# Display the selected analysis
if option3 == "Publication Frequency and publication Time":
    st.subheader("Publication Frequency and publication Time")
    publicationFrequency, publishingTimes = text_analyser.analyze_time_series()
    st.write(publicationFrequency)
    st.write(publishingTimes)

elif option3 == "Plot Time Series Trends":
    st.subheader("Plot Time Series Trends")
    publicationFrequency, publishingTimes = text_analyser.analyze_time_series()
    trend=text_analyser.plot_time_series_trends(publicationFrequency, publishingTimes)
    st.pyplot(trend)