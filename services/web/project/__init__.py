from flask import Flask, request, jsonify
from project.utils.execute_nfl_api import ExecuteNflApi

app = Flask(__name__)
app.config.from_pyfile("config.py")


@app.route("/")
def fetch_nfl_events_data():
    form_data = dict(request.form)
    if len(form_data) == 3:

        execute_nfl_api = ExecuteNflApi(form_data)
        result = execute_nfl_api.main()

        return jsonify(result)

    return jsonify(
        message="received invalid data",
        category="error",
        status=400)


