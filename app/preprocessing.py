import re
import numpy as np
import pandas as pd

def convert_to_float(val):
    if val:
        if isinstance(val,str):
            return float(re.sub(r'[^0-9.]', '', val))
        if isinstance(val,float) or isinstance(val,int):
            return val
        elif np.isnan(val):
            return np.nan
    return np.nan

def convert_to_int(val):
    if val:
        if isinstance(val,str):
            return int(re.sub(r'[^0-9.]', '', val))
        elif isinstance(val,int):
            return val
        elif np.isnan(val):
            return np.nan
    return np.nan

def get_reviews(x):
    if isinstance(x, list) and len(x) == 2:
        return int(re.sub(r'[^0-9.]', '', x[1]))
    elif isinstance(x,list) and len(x) == 1:
        return np.nan
    elif isinstance(x,int):
        return x
    elif isinstance(x, str):
        return int(re.sub(r'[^0-9.]', '', x))
    else:
        return np.nan

def clean_reviews(x):
    if not x:
        return np.nan
    elif isinstance(x,int):
        return x
    elif isinstance(x, str):
        val = x.split()[0]
        return int(re.sub(r'[^0-9.]', '', val))
    else:
        return np.nan

def dataset_review_rating_fixers(dataset):
    null_reviews = dataset['total_reviews'].isnull()
    null_ratings = dataset.total_rating.isnull()
    mixed_ratings = dataset[~null_ratings].total_rating.str.contains('&')
    dataset['total_reviews']=dataset[null_reviews & mixed_ratings]['total_rating'].str.split('&').apply(get_reviews)
    dataset['total_rating'] = dataset['total_rating'].apply(clean_reviews)
    return dataset

def format_fixer(dataset):
    dataset.price = dataset.price.apply(convert_to_float)
    dataset.rating = dataset.rating.apply(convert_to_float)
    return dataset