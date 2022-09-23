from app.repositories.models import BeverageDetail
from ..repositories.managers import OrderDetailManager, BeverageDetailManager ,OrderManager
from .base import BaseController

class ReportController(BaseController):
    manager = OrderDetailManager

    @staticmethod
    def generate():
        most_requested_ingredients = OrderDetailManager.get_most_requestd() 
        most_requested_beverages = BeverageDetailManager.get_most_requestd()
        return {
            'most_requested_ingredient': most_requested_ingredients[0] or [],
            'most_requested_beverage': most_requested_beverages[0] or []
            }, None