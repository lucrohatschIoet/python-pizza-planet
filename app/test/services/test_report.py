from datetime import datetime
from typing import Counter
import pytest
from statistics import mode
import collections


def __report_values(client, orders, order_uri):
    clients = []
    ingredients = []
    beverages = []
    months = []
    for order in orders:
        order = order
        order_id = order.get('_id')
        order_detail = client.get(f'{order_uri}id/{order_id}')
        order_detail = order_detail.json
        clients.append(order_detail.get('client_name'))
        new_ingredient = [ingredient['ingredient']['name'] for ingredient in order_detail['ingradient_detail']]
        ingredients.append(new_ingredient[0])
        new_beverage = [beverage['beverage']['name'] for beverage in order_detail['beverage_detail']]
        beverages.append(new_beverage[0])
        months.append(order_detail['date'].split("-")[1])
    result ={
        'most_requested_ingredient': {'name': mode(ingredients), 'requested_times': ingredients.count(mode(ingredients))},
        'most_requested_beverage': {'name': mode(beverages), 'requested_times': beverages.count(mode(beverages))},
    }
    return result

def test_report_response(client, report_uri, create_report_orders):
    response = client.get(report_uri)
    pytest.assume(response.status.startswith('200'))
    piza_report = response.json
    pytest.assume(piza_report['most_requested_ingredient'])
    pytest.assume(piza_report['most_requested_beverage'])
    pytest.assume(piza_report['month_major_revenue'])
    pytest.assume(piza_report['top_three_clients'])

def test_report_service(client, report_uri, create_report_orders, order_uri):
    response = client.get(report_uri)
    pytest.assume(response.status.startswith('200'))
    piza_report = response.json
    orders = [order.json for order in create_report_orders]
    report = __report_values(client, orders, order_uri)
    print(piza_report['most_requested_ingredient']['name'])
    print(report['most_requested_ingredient']['name'])
    pytest.assume(piza_report['most_requested_ingredient']['name'] == report['most_requested_ingredient']['name'])
    pytest.assume(piza_report['most_requested_ingredient']['requested_times'] == report['most_requested_ingredient']['requested_times'])
    pytest.assume(piza_report['most_requested_beverage']['name'] == report['most_requested_beverage']['name'])
    pytest.assume(piza_report['most_requested_beverage']['requested_times'] == report['most_requested_beverage']['requested_times'])
