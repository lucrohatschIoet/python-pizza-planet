from app.common.http_methods import GET, POST
from flask import Blueprint, request

from .base_handler import handler
from ..controllers import OrderController

order = Blueprint('order', __name__)


@order.route('/', methods=POST)
def create_order():
    return handler(OrderController.create(request.json))


@order.route('/id/<_id>', methods=GET)
def get_order_by_id(_id: int):
    return handler(OrderController.get_by_id(_id))


@order.route('/', methods=GET)
def get_orders():
    return handler(OrderController.get_all())
