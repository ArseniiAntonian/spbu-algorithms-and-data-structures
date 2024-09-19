import generate
import random
from data import shops, pm_sys

class Buy:
    def __init__(self):
        self.quantity = generate.generate_quantity()
        self.department = generate.generate_department()
        self.shop = generate.generate_shop(self.department)
        self.category = generate.generate_categories(self.department)
        self.brand = generate.generate_brands(self.category, self.department)
        self.cost = generate.generate_cost(self.category, self.department) * self.quantity
        self.time = generate.generate_random_datetime()
        self.coordinates = random.choice(shops[self.department][self.shop])
        self.card_number = self.Card().generate_bank_card_number()
        

    class Card:
            def __init__(self):
                self.payment_system = random.choice(['МИР', 'MasterCard', 'Visa'])
                self.bank = random.choice(['Сбер', 'Т-банк', 'Сбер', 'ВТБ', 'Альфа банк'])
                self.pre = pm_sys[self.payment_system][self.bank]
                self.bank_card_number = self.generate_bank_card_number()

            def generate_bank_card_number(self):
                bank_card_number = f"{self.pre}{random.randint(10**11, 10**12 - 1)}"  
                return bank_card_number
