from api.controllers import (
    ExportScoreCardController
)
from api.helpers import parse_flask_request
from api.protocols import Controller
from api.utils import JinjaTemplateRender, WeasyPrintExporter 

from flask import Flask, jsonify, make_response, request
from flask.wrappers import Request


app      = Flask(__name__)
exporter = WeasyPrintExporter()
template = JinjaTemplateRender()


def make_json_response(controller: Controller, request: Request):
    response = controller.handle(parse_flask_request(request))
    flask_response = jsonify(response.body)
    flask_response.headers.update(**response.headers)
    return flask_response, response.status_code

def make_pdf_response(controller: Controller, request: Request):
    response = controller.handle(parse_flask_request(request))

    flask_response = None
    
    if(response.is_ok):
        flask_response = make_response(response.body['pdf'])
    else:
        flask_response = jsonify(response.body)
    
    flask_response.headers.update(**response.headers)
    return flask_response, response.status_code


@app.route('/', methods=['GET'])
def index():
    return jsonify({'data': 'Ok'}), 200


@app.route('/scorecard.pdf', methods=['POST'])
def export_scorecard():
    controller = ExportScoreCardController(template, exporter)
    return make_pdf_response(controller, request)


if(__name__=='__main__'):
    app.run(host='0.0.0.0', port=8000)
