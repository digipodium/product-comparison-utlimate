import pandas as pd
import plotly
import seaborn as sns
import plotly.express as px
from app import preprocessing as pp
from app import db
import numpy as np

def load_data(db,table_name="scraped_data"):
    dataset = pd.read_sql(table_name,db.engine,parse_dates=['created_on'],index_col='id')
    dataset = pp.dataset_review_rating_fixers(dataset)
    dataset = pp.format_fixer(dataset)
    dataset.replace(np.nan, 0, inplace=True)
    return dataset

def max_price_data(dataset,kw="mobiles"):
    data = dataset[dataset['keyword'] == kw]
    output = data.loc[data['price'].idxmax()]
    return output


def min_price_data(dataset,kw="mobiles"):
    data = dataset[dataset['keyword'] == kw]
    output = data.loc[data['price'].idxmin()]
    return output    

def max_reviews_data(dataset,kw="mobiles"):
    data = dataset[dataset['keyword'] == kw]
    print(data)
    output = data.loc[data['total_reviews'].idxmax()]
    return output    

def min_reviews_data(dataset,kw="mobiles"):
    data = dataset[dataset['keyword'] == kw]
    output = data.loc[data['total_reviews'].idxmin()]
    return output    

def max_ratings_data(dataset,kw="mobiles"):
    data = dataset[dataset['keyword'] == kw]
    output = data.loc[data['rating'].idxmax()]
    return output    

def min_ratings_data(dataset,kw="mobiles"):
    data = dataset[dataset['keyword'] == kw]
    output = data.loc[data['rating'].idxmin()]
    return output    

def total_data(dataset,kw='mobiles'):
    data = dataset[dataset['keyword'] == kw]
    return data.shape[0]

def total_data_per_website(dataset,kw='mobiles'):
    data = dataset[dataset['keyword'] == kw]
    return data.website.value_counts()

def total_price(dataset,kw='mobiles'):
    data = dataset[dataset['keyword'] == kw]
    return data.price.sum()

def total_reviews(dataset,kw='mobiles'):
    data = dataset[dataset['keyword'] == kw]
    return data.total_reviews.sum()

def total_rating(dataset,kw='mobiles'):
    data = dataset[dataset['keyword'] == kw]
    return data.total_rating.sum()


if __name__ == "__main__":
    kw = 'headphones'
    dataset = load_data(db)
    kList = dataset.keyword.unique()
    maxprice = max_price_data(dataset,kw)
    minprice= min_price_data(dataset,kw)
    maxrating = max_ratings_data(dataset,kw)
    minrating = min_ratings_data(dataset,kw)
    totdata =total_data(dataset,kw)
    totprice = total_price(dataset,kw)
    totreviews = total_reviews(dataset,kw)
    totrating = total_rating(dataset,kw)
    print(maxprice)
    print(minprice)
    print(maxrating)
    print(minrating)
    print(totdata)
    print(totreviews)
    print(totrating)

