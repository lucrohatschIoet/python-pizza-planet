from app.repositories.models import BeverageDetail
from ..repositories.managers import OrderDetailManager, BeverageDetailManager ,OrderManager
from .base import BaseController

class ReportController(BaseController):
    manager = OrderDetailManager

    @staticmethod
    def generate():
        most_requested_ingredients = OrderDetailManager.get_most_requestd() 
        most_requested_beverages = BeverageDetailManager.get_most_requestd()
        major_revenue_per_month = OrderManager.get_revenue_per_month()
        clients_order_ranking = OrderManager.get_clients_order_ranking()
        return {
            'most_requested_ingredient': most_requested_ingredients[0] or [],
            'most_requested_beverage': most_requested_beverages[0] or [],
            'month_major_revenue': major_revenue_per_month[0],
            'top_three_clients':clients_order_ranking[:3]

            }, None