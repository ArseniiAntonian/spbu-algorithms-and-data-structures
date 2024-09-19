import random
from data import low_price_category, medium_price_category, high_price_category, shops

from datetime import datetime, timedelta

def generate_random_datetime():
    delta_days = (datetime(2024, 9, 15) - datetime(2020, 1, 1)).days
    random_days = random.randint(0, delta_days)
    random_date = datetime(2020, 1, 1) + timedelta(days=random_days)
    random_time = timedelta(hours=random.randint(10-3, 21-3), minutes=random.randint(0, 59), seconds=random.randint(0,59))
    full_datetime = random_date + random_time
    
    return f"{full_datetime.isoformat()}+3:00"

time = generate_random_datetime()

def generate_department():
    departments = list(shops.keys())
    return random.choice(departments)

department = generate_department()

def generate_shop(department):
    second_level_dict = shops[department]
    second_level_keys = list(second_level_dict.keys())
    return random.choice(second_level_keys)

shop = generate_shop(department)


def generate_categories(department):
    return random.choice(list(medium_price_category[department].keys()) + list(low_price_category[department].keys()) + list(high_price_category[department].keys()))

category = generate_categories(department)

def generate_brands(category):
    if category in list(low_price_category.keys()):
        return random.choice(low_price_category[category])
    elif category in list(medium_price_category.keys()):
        return random.choice(medium_price_category[category])
    elif category in list(high_price_category.keys()):
        return random.choice(high_price_category[category])
    
brand = generate_brands(category)

def generate_quantity():
    return random.randint(1, 5)

def generate_cost(category, department):
    if category in list(low_price_category[department].keys()):
        return random.randint(100, 5000)
    elif category in list(medium_price_category[department].keys()):
        return random.randint(5001, 20000)
    elif category in list(high_price_category[department].keys()):
        return random.randint(20001, 70000)
    
cost = generate_cost(category, department)

print(f"time: {time}, department: {department}, shop: {shop}, category: {category}, cost: {cost}")
    