import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from assignment1 import data
import pandas as pd

def calculate_k_anonymity(df, quasi_identifiers, n):
    group_counts = df.groupby(quasi_identifiers, observed = True).size()
    k = sorted(group_counts)[:n]
    return k

def calculate_k_anonymity(df, quasi_identifiers, n, total_length=50000):
    
    group_counts = df.groupby(quasi_identifiers, observed=True).size()
    

    unique_k_values = sorted(group_counts.unique())
    
    top_k_values = unique_k_values[:n]
    
    percentages = [(k_value, (group_counts == k_value).sum() / len(df) * 100) for k_value in top_k_values]
    
    print(f"Топ {n} уникальных значений k-анонимности:")
    for k_value, percentage in percentages:
        print(f"K = {k_value}, Процент = {percentage:.2f}%")
    
    return top_k_values


def cost_depersonalization(df : pd.DataFrame):
    bins=[100, 10000, 100000, 1000000, 5000000]
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
    bins = [5, 10, 30, 60, 100]
    labels = [f'{bins[i]}-{bins[i + 1]}' for i in range(len(bins) - 1)]
    df['quantity'] = pd.cut(df['quantity'], bins=bins, labels=labels, include_lowest=True)

    return df

def brand_depersonalization(df: pd.DataFrame):
    df = df.drop(columns=['brand'])
    return df

def card_number_depersonalization(df: pd.DataFrame):
    # number_to_info = {}
    # for system, banks in data.pm_sys.items():
    #     for bank, pre in banks.items():
    #         number_to_info[pre] = (bank, system)

    # df['card_info'] = df['card_number'].apply(lambda x: number_to_info.get(str(x)[:4]))
    # df['bank'], df['payment_system'] = zip(*df['card_info'])
    # df = df.drop(columns=['card_info', 'card_number'])

    def mask_card_number(card_number):
        card_str = str(card_number)  
        
        return card_str[:2] + 'X' * (len(card_str) - 2)
    df['card_number'] = df['card_number'].apply(mask_card_number)
    
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
    category_generalization = {
        "флешка": "Компьютерные аксессуары",
        "зарядное устройство": "Компьютерные аксессуары",
        "наушники": "Компьютерные аксессуары",
        "сетевой фильтр": "Компьютерные аксессуары",
        "мышь": "Компьютерные аксессуары",
        "клавиатура": "Компьютерные аксессуары",
        "модем": "Сетевое оборудование",
        "триммер": "Бытовая техника",
        "фен": "Бытовая техника",
        "блендер": "Кухонная техника",
        "электрическая зубная щетка": "Бытовая техника",
        "умная колонка": "Умная техника",
        "веб-камера": "Компьютерные аксессуары",
        "пауэрбанк": "Компьютерные аксессуары",
        "фитнес-браслет": "Умная техника",
        "роутер": "Сетевое оборудование",
        "корм для кошек": "Товары для животных",
        "корм для собак": "Товары для животных",
        "сухофрукты": "Продукты питания",
        "консервированные овощи": "Продукты питания",
        "холодные напитки": "Продукты питания",
        "слабоалкогольные напитки": "Напитки",
        "вода": "Напитки",
        "фрукты": "Продукты питания",
        "овощи": "Продукты питания",
        "внешний жесткий диск": "Компьютерные аксессуары",
        "умные часы": "Умная техника",
        "проектор": "Мультимедиа",
        "акустическая система": "Мультимедиа",
        "SSD-накопитель": "Компьютерные аксессуары",
        "мультимедийный плеер": "Мультимедиа",
        "видеокарта": "Компьютерные комплектующие",
        "оперативная память": "Компьютерные комплектующие",
        "материнская плата": "Компьютерные комплектующие",
        "процессор": "Компьютерные комплектующие",
        "ИБП (источник бесперебойного питания)": "Компьютерные аксессуары",
        "игровая гарнитура": "Компьютерные аксессуары",
        "умный дом": "Умная техника",
        "система видеонаблюдения": "Умная техника",
        "кофеварка": "Кухонная техника",
        "игрушки для животных": "Товары для животных",
        "премиум-корм": "Товары для животных",
        "свежее мясо": "Продукты питания",
        "морепродукты": "Продукты питания",
        "виски": "Алкогольные напитки",
        "вино": "Алкогольные напитки",
        "водка": "Алкогольные напитки",
        "шампанское": "Алкогольные напитки",
        "монитор": "Компьютерные аксессуары",
        "принтер": "Офисное оборудование",
        "сканер": "Офисное оборудование",
        "смартфон": "Мобильные устройства",
        "планшет": "Мобильные устройства",
        "ноутбук": "Мобильные устройства",
        "настольный компьютер": "Компьютеры",
        "фотоаппарат": "Мультимедиа",
        "видеокамера": "Мультимедиа",
        "телевизор": "Мультимедиа",
        "игровая консоль": "Мультимедиа",
        "кондиционер": "Бытовая техника",
        "3D-принтер": "Офисное оборудование",
        "холодильник": "Бытовая техника",
        "стиральная машина": "Бытовая техника",
        "пылесос": "Бытовая техника",
        "микроволновая печь": "Кухонная техника",
        "системный блок": "Компьютеры",
        "кухонная техника": "Кухонная техника",
        "утюг": "Бытовая техника",
        "высококачественная мебель для животных": "Товары для животных",
        "элитные алкогольные напитки": "Алкогольные напитки",
        "редкие деликатесы": "Продукты питания"
    }

    df['category'] = df['category'].map(category_generalization).fillna(df['category'])
    return df

def remove_unique_rows(df, max_removal=2500):
    duplicated_df = df[df.duplicated(keep=False)]
    unique_rows = df[~df.index.isin(duplicated_df.index)]
    if len(unique_rows) > max_removal:
        unique_rows = unique_rows.iloc[:max_removal]
    df_cleaned = df.drop(unique_rows.index)
    
    return df_cleaned
