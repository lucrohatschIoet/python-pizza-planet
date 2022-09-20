from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from .base_handler import handler
from ..controllers import IngredientController

ingredient = Blueprint('ingredient', __name__)


@ingredient.route('/', methods=POST)
def create_ingredient():
    return handler(IngredientController.create(request.json))


@ingredient.route('/', methods=PUT)
def update_ingredient():
    return handler(IngredientController.update(request.json))


@ingredient.route('/id/<_id>', methods=GET)
def get_ingredient_by_id(_id: int):
    return handler(IngredientController.get_by_id(_id))


@ingredient.route('/', methods=GET)
def get_ingredients():
    return handler(IngredientController.get_all())
