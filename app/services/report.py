from app.common.http_methods import GET
from flask import Blueprint

from ..controllers import ReportController
from .base_handler import handler

report = Blueprint('report', __name__)


@report.route('/', methods=GET)
def get_report():
    return handler(ReportController.generate())
