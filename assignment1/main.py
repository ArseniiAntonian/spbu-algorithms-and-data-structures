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
    payment_systems = ['МИР', 'MasterCard', 'Visa']
    banks = ['Сбер', 'Т-банк', 'ВТБ', 'Альфа банк']
    pm_sys_weights = []
    bank_weights = []

    for i in range(3):
        print(f"Введите вес для платежной системы {payment_systems[i]}: ")
        weight = float(input())
        pm_sys_weights.append(weight)

    for i in range(4):
        print(f"Введите вес для банка {banks[i]}: ")
        weight = float(input())
        bank_weights.append(weight)
    
    start_time = time.time()
    data = generate_data(100000, pm_sys_weights, bank_weights)
    df = pd.DataFrame(data)
    end_time = time.time()

    
    df.to_xml('assignment1/purchases.xml', index=False, encoding='utf-8', root_name='purchases', row_name='purchase')
    print(f"Сгенерирован за {(end_time - start_time):.2f}")
    print(df.head(10))