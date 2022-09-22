from ..repositories.managers import OrderManager


class ReportController:

    @staticmethod
    def generate():
        orders = OrderManager.get_all()
        return {'report': orders}, None