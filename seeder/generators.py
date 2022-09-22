from datetime import datetime

from faker import Faker

fake = Faker()


def generate_clientes(n: int) -> list[dict]:
    clients = []
    for i in range(n):
        client = {
            'client_name': fake.name(), 
            'client_dni': fake.pyint(min_value=20000000, max_value=50000000), 
            'client_address': fake.address(), 
            'client_phone': fake.phone_number(), 
        }
        clients.append(client)
    return clients


def generate_date() -> datetime:
    random_date =fake.date_time_between(
        start_date=datetime(2022, 1, 1),
        end_date=datetime.now()
    )
    return random_date


def generate_price(min:float, max:float) -> float:
    price = fake.pyfloat(
        right_digits=2,
        positive=True,
        min_value=min,
        max_value=max
    )
    return price


ingredients = [
    'muzzarella',
    'pepperoni',
    'olives',
    'parmesan',
    'tomato',
    'bacon',
    'sausage',
    'parsley',
    'red onion',
    'artichokes',
    'basil',
    'red pepper',
    'greek',
    'cheddar',
    'egg',
    'ham',
    'pineapple'
]

sizes = [
    'slice',
    'personal (10 in)',
    'small (12 in)',
    'medium (14 in)',
    'large (16 in)',
    'x-large (18 in)'
]

beverages = [
    'blond beer',
    'cola',
    'lemonade',
    'iced tea',
    'water',
    'soda',
    'wine'
]
