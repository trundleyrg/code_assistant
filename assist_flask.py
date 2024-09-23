"""
restful api
"""

from flask import Flask, request
from flask_cors import CORS

from code_assistant import CodeAssistant
from utils.setting import SERVER_PORT

app = Flask(__name__)
ca = CodeAssistant()

# 允许所有来源的跨域请求
CORS(app)


@app.route('/write_code', methods=['POST'])
def set_title():
    request_data = request.get_json()
    if "data" not in request_data:
        return
    return ca.write_code(request_data["data"])


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=SERVER_PORT)
