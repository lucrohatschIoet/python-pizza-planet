from app.common.http_methods import GET
from flask import Blueprint

from .base_handler import handler
from ..controllers import ReportController

report = Blueprint('report', __name__)

@report.route('/', methods=GET)
def get_report():
    return handler(ReportController.generate())
