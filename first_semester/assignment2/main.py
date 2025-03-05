import pandas as pd
import functions as fun

df = pd.read_xml("assignment1/purchases.xml")

if input('Обезличить название магазина? [y/n]') == 'y':
    df = fun.shop_depersonalization(df)
if input('Обезличить координаты магазина? [y/n]') == 'y':
    df = fun.coords_depersonalization(df)
if input('Обезличить время покупки? [y/n]') == 'y':
    df = fun.time_depersonalization(df)
if input('Обезличить категорий товара? [y/n]') == 'y':
    df = fun.category_depersonalization(df)
if input('Обезличить бренд товара? [y/n]') == 'y':
    df = fun.brand_depersonalization(df)
if input('Обезличить номер карты? [y/n]') == 'y':
    df = fun.card_number_depersonalization(df)
if input('Обезличить количество товаров? [y/n]') == 'y':
    df = fun.quantity_depersonalization(df)
if input('Обезличить стоимость покупки? [y/n]') == 'y':
    df = fun.cost_depersonalization(df)

print(df.head(10))
fun.calculate_k_anonymity(df, list(df.columns), 5)
df.to_xml('assignment2/depersonalized_purchases.xml', index=False, encoding='utf-8', root_name='purchases', row_name='purchase')