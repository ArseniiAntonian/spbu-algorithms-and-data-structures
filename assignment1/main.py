import pandas as pd
from buy import Buy

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
    n = int(input("Введите количество строк (минимум 50000) :"))
    if n < 50000:
        print('Количество строк не может быть менее 50000. Установлено значение 50000')
        n = 50000
    data = generate_data(n, pm_sys_weights, bank_weights)
    df = pd.DataFrame(data)

    df.to_xml('assignment1/purchases.xml', index=False, encoding='utf-8', root_name='purchases', row_name='purchase')
    print("Датасет сгенерирован")