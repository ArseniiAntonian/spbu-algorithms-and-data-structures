import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from assignment1 import data
import pandas as pd

def calculate_k_anonymity(df, quasi_identifiers, n):
    
    group_counts = df.groupby(quasi_identifiers, observed=True).size()
    unique_k_values = sorted(group_counts.unique())
    top_k_values = unique_k_values[:n]
    percentages = [(k_value, (group_counts == k_value).sum() / len(df) * 100) for k_value in top_k_values]

    print(f"Топ {n} уникальных значений k-анонимности:")
    for k_value, percentage in percentages:
        print(f"K = {k_value}, Процент = {percentage:.4f}%")


def cost_depersonalization(df : pd.DataFrame):
    bins=[100, 10000, 500000, 2000000]
    labels = [f'{bins[i]}-{bins[i+1]}' for i in range(len(bins)-1)]
    df['cost'] = pd.cut(df['cost'], bins=bins, labels=labels, include_lowest=True)
    return df

def shop_depersonalization(df : pd.DataFrame):
    shop_to_theme = {}
    for theme, stores in data.shops.items():
        for store_name in stores:
            shop_to_theme[store_name] = theme
    df['shop'] = df['shop'].map(shop_to_theme)

    df.rename(columns={'shop' : 'theme'}, inplace=True)
    
    return df

def quantity_depersonalization(df: pd.DataFrame):
    bins = [5, 20]
    labels = [f'{bins[i]}-{bins[i + 1]}' for i in range(len(bins) - 1)]
    df['quantity'] = pd.cut(df['quantity'], bins=bins, labels=labels, include_lowest=True)
    return df

def brand_depersonalization(df: pd.DataFrame):
    df = df.drop(columns=['brand'])
    return df

def card_number_depersonalization(df: pd.DataFrame):
    number_to_info = {}
    for system, banks in data.pm_sys.items():
        for bank, pre in banks.items():
            number_to_info[pre] = (bank, system)

    df['card_info'] = df['card_number'].apply(lambda x: number_to_info.get(str(x)[:4]))
    df['bank'], _ = zip(*df['card_info'])
    df = df.drop(columns=['card_info', 'card_number'])
    
    return df

def coords_depersonalization(df: pd.DataFrame):
    df['coordinates'] = 'Санкт-Петербург'
    df.rename(columns={'coordinates' : 'state'}, inplace=True)
    return df

def time_depersonalization(df: pd.DataFrame):
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df['time'] = df['time'].dt.year
    return df

def category_depersonalization(df: pd.DataFrame):
    df = df.drop(columns=['category'])
    return df
