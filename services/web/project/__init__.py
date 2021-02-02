from flask import Flask, request, jsonify
import logging.handlers

import project.constants as const


app = Flask(__name__)

from project.utils.execute_nfl_api import ExecuteNflApi
from project.utils.validate_request import ValidateRequest
from project.tests.test_endpoint import TestEndPoint

app.config.from_pyfile("config.py")

handler = logging.FileHandler(const.LOG_FILE)
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))
app.logger.addHandler(handler)


@app.route("/", methods=['GET'])
def fetch_nfl_events_data():
    form_data = dict(request.form)
    validator = ValidateRequest()
    if validator.validator(form_data):

        execute_nfl_api = ExecuteNflApi(form_data)
        result = execute_nfl_api.main()

        return jsonify(result)

    return jsonify(message="received invalid data"), 400
