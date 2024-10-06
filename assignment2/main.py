import pandas as pd
import functions as fun

df = pd.read_xml("assignment1/purchases.xml")

print(f"K-anonymity до обезличивания: {fun.calculate_k_anonymity(df, list(df.columns), 1)}")
quasies = []

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
df = fun.remove_unique_rows(df)
k_values = fun.calculate_k_anonymity(df, list(df.columns), 5)
print(f"K-anonymity после обезличивания : {k_values}")
# total_records = len(df)
# percentages = [(k / total_records) * 100 for k in k_values]
# print("\nПроцентное соотношение первых K-анонимностей:")
# print(percentages)
df.to_xml('assignment2/depersonalized_purchases.xml', index=False, encoding='utf-8', root_name='purchases', row_name='purchase')