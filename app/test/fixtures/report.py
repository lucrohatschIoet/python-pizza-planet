import pytest

from ..utils.functions import shuffle_list

def report_mock() -> dict:
    return {
        'most_requested_ingredient': {'name': 'tomato', 'requested_times': 50},
        'most_requested_beverage': {'name': 'beer', 'requested_times': 20},
        'month_major_revenue': {'name': 'jly', 'revenue': 120.2},
        'top_three_clients': [
            {'name': 'lucas', 'orders': 50}, 
            {'name': 'miguel', 'orders': 15}, 
            {'name': 'miguel', 'orders': 10}]
    }

@pytest.fixture
def report_uri():
    return '/report/'

@pytest.fixture
def create_report_client():
    clients = [
        {
        'client_address': '399 Murphy Junction',
        'client_dni': 37295675,
        'client_name': 'Charles Simmons',
        'client_phone': 6945117592
        },
        {
        'client_address': '0717 Christina Junction',
        'client_dni': 21675330,
        'client_name': 'Kevin Baker',
        'client_phone': 7375931105
        }
    ]
    return clients

@pytest.fixture
def create_report_ingredients(client, ingredient_uri):
    ingredients = [
        {
            'name':'tomato',
            'price': 1.2
        },
        {
            'name':'muzzarella',
            'price': 2
        },
        {
            'name':'olive',
            'price': 0.5
        }
    ]
    creates = [client.post(ingredient_uri, json=ingredient) for ingredient in ingredients]
    return creates


@pytest.fixture
def create_report_beverages(client, beverage_uri):
    beverages = [
        {
            'name':'beer',
            'price': 1.2
        },
        {
            'name':'water',
            'price': 2
        }
    ]

    creates = [client.post(beverage_uri, json=beverage) for beverage in beverages]
    return creates
    
@pytest.fixture
def create_report_sizes(client, size_uri):
    sizes = [
        {
            'name':'small',
            'price': 1
        }
    ]
    creates = [client.post(size_uri, json=size) for size in sizes]
    return creates


@pytest.fixture
def create_report_orders(client, order_uri, create_report_ingredients, create_report_beverages, create_report_sizes, create_report_client):
    ingredients = [ingredient.json.get('_id') for ingredient in create_report_ingredients]
    print(ingredients)
    beverages = [beverage.json.get('_id') for beverage in create_report_beverages]
    sizes = [size.json.get('_id') for size in create_report_sizes]

    orders = []
    for _ in range(10):
        order_client = shuffle_list(create_report_client)[0]
        new_order = client.post(order_uri, json={
            **order_client,
            'ingredients': shuffle_list(ingredients)[2:3],
            'beverages': [shuffle_list(beverages)[0]],
            'size_id': shuffle_list(sizes)[0]
        })
        orders.append(new_order)
    return orders


@pytest.fixture
def create_report(client, create_report_orders, report_uri):
    report = client.get(report_uri).json
    return report