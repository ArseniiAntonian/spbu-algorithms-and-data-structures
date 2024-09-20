import pandas as pd
from buy import Buy
import time

def generate_data(n, pm_sys_weights, bank_weights):
    data = []
    for _ in range(n):
        buy = Buy(pm_sys_weights, bank_weights)
        record = {
            'shop': buy.shop,
            'coordinates': buy.coordinates,
            'time': str(buy.time),
            'category': buy.category,
            'brand': buy.brand,
            'card_number': buy.card_number,
            'quantity': buy.quantity,
            'cost': buy.cost          
        }
        data.append(record)
    return data

if __name__ == "__main__": 

    start_time = time.time()

    pm_sys_weights = []
    bank_weights = []

    print("Введите веса для платежных систем 'МИР', 'MasterCard', 'Visa'")

    for i in range(3):
        weight = float(input())
        pm_sys_weights.append(weight)

    print("Введите веса для банков 'Сбер', 'Т-банк', 'ВТБ', 'Альфа банк'")

    for i in range(4):
        weight = float(input())
        bank_weights.append(weight)
    
    data = generate_data(100000, pm_sys_weights, bank_weights)
    df = pd.DataFrame(data)
    end_time = time.time()

    
    df.to_csv('assignment1\purchases.csv', index=False, encoding='utf-8')
    print(f"Сгенерирован за {(end_time - start_time):.2f}")
    print(df.head(10))