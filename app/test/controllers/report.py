import pytest
from app.controllers import ReportController

def test_generate_report(app):
    report = ReportController.generate()
    pytest.assume(report['most_requested_ingredient'])
    pytest.assume(report['most_requested_ingredient']['name'])
    pytest.assume(report['most_requested_beverage'])
    pytest.assume(report['most_requested_beverage']['name'])
    pytest.assume(report['month_major_revenue'])
    pytest.assume(report['month_major_revenue']['name'])
    pytest.assume(report['top_three_clients'])