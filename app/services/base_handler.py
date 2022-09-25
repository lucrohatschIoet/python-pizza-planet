from flask import jsonify


def handler(controller_method):
    service_object, error = controller_method
    response = service_object if not error else {'error': error}
    status_code = 200 if service_object else 404 if not error else 400
    return jsonify(response), status_code
