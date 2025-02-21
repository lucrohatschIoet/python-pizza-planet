
import pytest


def test_get_order_service(client, create_orders, order_uri):
    response = client.get(order_uri)
    pytest.assume(response.status.startswith('200'))
    returned_orders = {order['_id']: order for order in response.json}
    for order in create_orders:
        pytest.assume(order.json['_id'] in returned_orders)

def test_create_order_service(create_orders):
    first_order = create_orders[0]
    order = first_order.json
    pytest.assume(first_order.status.startswith('200'))
    pytest.assume(order['_id'])
    pytest.assume(order['client_dni'])
    pytest.assume(order['client_name'])
    pytest.assume(order['client_phone'])

def test_get_order_by_id_service(client, create_orders, order_uri):
    current_ingredient = create_orders[0].json
    response = client.get(f'{order_uri}id/{current_ingredient["_id"]}')
    pytest.assume(response.status.startswith('200'))
    returned_orders = response.json
    for param, value in current_ingredient.items():
        pytest.assume(returned_orders[param] == value)
