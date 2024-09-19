import pandas as pd
from buy import Buy
import time

def generate_data(n):
    data = []
    for _ in range(n):
        buy = Buy()
        record = {
            'quantity': buy.quantity,
            'department': buy.department,
            'shop': buy.shop,
            'category': buy.category,
            'brand': buy.brand,
            'cost': buy.cost,
            'time': str(buy.time),
            'coordinates': buy.coordinates,
            'card_number': buy.card_number
        }
        data.append(record)
    return data

if __name__ == "__main__": 

    start_time = time.time()
    data = generate_data(500000)
    df = pd.DataFrame(data)
    end_time = time.time()

    print(f"Сгенерирован за {(end_time - start_time):.2f}")
    df.to_csv('1\purchases.csv', index=False, encoding='utf-8')
    print(df.head(10))