from random import choice, randint, sample

from app import create_app
from app.repositories.managers import (BeverageManager, IngredientManager,
                                       OrderManager, SizeManager)

from seeder.generators import (beverages, generate_clientes, generate_date,
                               generate_price, ingredients, sizes)

app = create_app('app.settings.Config')
app.app_context().push()

def calculate_order_price(size_price: float, ingredients: list, beverages: list):
        ingredient_price = sum(ingredient.price for ingredient in ingredients)
        beverages_price = sum(beverage.price for beverage in beverages)
        total_price = ingredient_price + beverages_price  + size_price
        return round(total_price, 2)

def seed_sizes():
    for size in sizes:
        seed = {
            'name': size,
            'price': generate_price(3,8)
        }
        SizeManager.create(seed)

def seed_ingredients():
    for ingredient in ingredients:
        seed = {
            'name': ingredient,
            'price': generate_price(1,5)
        }
        IngredientManager.create(seed)

def seed_beverage():
    for beverage in beverages:
        seed = {
            'name': beverage,
            'price': generate_price(2,10)
        }
        BeverageManager.create(seed)

def seed_orders(n_clients:int, n_orders:int):
    clients = generate_clientes(n_clients)
    db_sizes = SizeManager.get_all()
    db_ingredients = IngredientManager.get_all()
    db_beverages = BeverageManager.get_all()
    for i in range(n_orders):
        client = choice(clients)
        order_data = client 
        size = choice(db_sizes)
        order_data['size_id'] = size['_id']
        order_data['date'] = generate_date()
        order_ingredients = sample(db_ingredients, randint(1,5))
        order_beverages = sample(db_beverages, randint(0,3))
        ingredients_list = IngredientManager.get_by_id_list([ingredient['_id'] for ingredient in order_ingredients])
        beverages_list = BeverageManager.get_by_id_list([beverage['_id'] for beverage in order_beverages])
        price = calculate_order_price(size['price'], ingredients_list, beverages_list)
        order_data['total_price'] = price
        OrderManager.create(order_data, ingredients_list, beverages_list)

def execute(n_clients:int, n_orders:int):
    seed_beverage()
    seed_ingredients()
    seed_sizes()
    seed_orders(n_clients, n_orders)

if __name__ == '__main__':
    execute(10,100)