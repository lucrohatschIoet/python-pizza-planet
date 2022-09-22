from datetime import datetime
from urllib import response
import pytest
from statistics import mode
from app.test.fixtures.ingredient import ingredient


def __report_values(client, orders, order_uri):
    clients = []
    ingredients = []
    beverages = []
    months = []
    for order in orders:
        order_id = order['_id']
        order_detail = client.get(f'{order_uri}id/{order_id}')
        clients.append(order_detail['client_name'])
        ingredients.append(ingredient['name'] for ingredient in order_detail['ingradient_detail'])
        beverages.append(beverage['name'] for beverage in order_detail['beverage_detail'])
        months.append(datetime.strptime(order_detail['date'], '%Y-%m-%dT%H:%M:%S').month)
    
    result ={
        'most_requested_ingredient': {'name': mode(ingredients), 'requested_times': ingredients.count(mode(ingredients))},
        'most_requested_beverage': {'name': mode(beverages), 'requested_times': beverages.count(mode(beverages))},
    }
    return result

def test_report_response(client, report_uri):
    response = client.get(report_uri)
    pytest.assume(response.status.startswith('200'))
    pytest.assume(response['most_requested_ingredient'])
    pytest.assume(response['most_requested_beverage'])
    pytest.assume(response['month_major_revenue'])
    pytest.assume(response['top_three_clients'])

def test_report_service(client, report_uri, create_report_orders, create_report):
    response = create_report
    pytest.assume(response.status.startswith('200'))
    report = __report_values(create_report_orders)
    
    pytest.assume(response['most_requested_ingredient']['name'] == report['most_requested_ingredient']['name'])
    pytest.assume(response['most_requested_ingredient']['requested_times'] == report['most_requested_ingredient']['requested_times'])
    pytest.assume(response['most_requested_beverage']['name'] == report['most_requested_beverage']['name'])
    pytest.assume(response['most_requested_beverage']['requested_times'] == report['most_requested_beverage']['requested_times'])
    
