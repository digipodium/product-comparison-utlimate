import pandas as pd
import plotly
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from app import preprocessing as pp


def load_data(db,table_name="scraped_data"):
    dataset = pd.read_sql(table_name,db.engine,parse_dates=['created_on'],index_col='id')
    dataset = pp.dataset_review_rating_fixers(dataset)
    dataset = pp.format_fixer(dataset)
    return dataset

def hist_comparison_of_item_prices(dataset, kw = 'bottles',x = 'price',facet_col='website',title=None ):
    data = dataset[dataset['keyword'] == kw]
    fig = px.histogram(data_frame = data, x = x, title = title, facet_col = facet_col, color='price', width=700, height=600)
    return fig.to_json()

def hist_comparison_of_item_total_ratings(dataset, kw='bottles',x = 'total_rating', facet_col='website', title=None):
    data = dataset[dataset['keyword'] == kw]
    fig = px.histogram(data_frame = data, x = x, title = title, facet_col = facet_col, color='price', width=700, height=600)
    return fig.to_json()

def hist_comparison_of_item_total_reviews(dataset, kw='bottles',x = 'total_reviews', facet_col='website', title=None):
    data = dataset[dataset['keyword'] == kw]
    fig = px.histogram(data_frame = data, x = x, title = title, facet_col = facet_col, color='price', width=700, height=600)
    return fig.to_json()

def hist_comparison_of_item_rating(dataset, kw='bottles',x = 'rating', facet_col='website', title=None):
    data = dataset[dataset['keyword'] == kw]
    fig = px.histogram(data_frame = data, x = x, title = title, facet_col = facet_col, color='price', width=700, height=600)
    return fig.to_json()

def bar_polar_price_distribution(dataset, kw = 'bottles', x = 'price',hover_name="website",title=None):
    data = dataset[dataset['keyword'] == kw]
    fig = px.bar_polar(data_frame = data,r=x,title=title, width=700, height=600, color=x, hover_name = hover_name)
    return fig.to_json()
