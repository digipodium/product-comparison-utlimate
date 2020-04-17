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
    fig = px.histogram(data_frame = data, x = x, title = title, facet_col = facet_col, color='price', width=500, height=500)
    return fig.to_json()

def hist_comparison_of_item_total_ratings(dataset, kw='bottles',x = 'total_rating', facet_col='website', title=None):
    data = dataset[dataset['keyword'] == kw]
    fig = px.histogram(data_frame = data, x = x, title = title, facet_col = facet_col, color='price', width=500, height=500)
    return fig.to_json()

def hist_comparison_of_item_total_reviews(dataset, kw='bottles',x = 'total_reviews', facet_col='website', title=None):
    data = dataset[dataset['keyword'] == kw]
    fig = px.histogram(data_frame = data, x = x, title = title, facet_col = facet_col, color='price', width=500, height=500)
    return fig.to_json()

def hist_comparison_of_item_rating(dataset, kw='bottles',x = 'rating', facet_col='website', title=None):
    data = dataset[dataset['keyword'] == kw]
    fig = px.histogram(data_frame = data, x = x, title = title, facet_col = facet_col, color='price', width=500, height=500)
    return fig.to_json()

def bar_polar_price_distribution(dataset, kw = 'bottles', x = 'price',hover_name="website",title=None):
    data = dataset[dataset['keyword'] == kw]
    fig = px.bar_polar(data_frame = data,r=x,title=title, width=500, height=500, color=x, hover_name = hover_name)
    return fig.to_json()

def bar_product_count(dataset,kw="bottles",title=None):
    data = dataset[dataset['keyword'] == kw]
    output = data.website.value_counts()
    fig = px.bar(x = output.index, y = output,title=f"{kw} counts comparison of websites".upper(),width=500, height=500)
    return fig.to_json()

def pie_product_avg_price(dataset,kw="bottles",title=None):
    data = dataset[dataset['keyword'] == kw]
    output_mean = data[['website','price']].groupby('website').mean()
    fig = px.pie(names = output_mean.index, values = output_mean,title=f"{kw} avg price comparison".upper(),width=500, height=500,color=output_mean)
    return fig.to_json()

def pie_product_max_price(dataset,kw="bottles",title=None):
    data = dataset[dataset['keyword'] == kw]
    output_mean = data[['website','price']].groupby('website').max()
    fig = px.pie(names = output_mean.index, values = output_mean,title=f"{kw} max price comparison".upper(),width=500, height=500,color=output_mean)
    return fig.to_json()

def pie_product_min_price(dataset,kw="bottles",title=None):
    data = dataset[dataset['keyword'] == kw]
    output_mean = data[['website','price']].groupby('website').min()
    fig = px.pie(names = output_mean.index, values = output_mean,title=f"{kw} min price comparison".upper(),width=500, height=500,color=output_mean)
    return fig.to_json()
    
def pie_product_std_price(dataset,kw="bottles",title=None):
    data = dataset[dataset['keyword'] == kw]
    output_mean = data[['website','price']].groupby('website').std()
    fig = px.pie(names = output_mean.index, values = output_mean,title=f"{kw} standard deviation in price".upper(),width=500, height=500,color=output_mean)
    return fig.to_json()
    