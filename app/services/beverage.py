from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from .base_handler import handler
from ..controllers import BeverageController

beverage = Blueprint('beverage', __name__)


@beverage.route('/', methods=POST)
def create_beverage():
    return handler(BeverageController.create(request.json))


@beverage.route('/', methods=PUT)
def update_beverage():
    return handler(BeverageController.update(request.json))


@beverage.route('/id/<_id>', methods=GET)
def get_beverage_by_id(_id: int):
    return handler(BeverageController.get_by_id(_id))


@beverage.route('/', methods=GET)
def get_beverage():
    return handler(BeverageController.get_all())
