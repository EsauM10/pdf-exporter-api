from flask.wrappers import Request as FlaskRequest

from typing import Any, Dict, List

from api.exceptions import BadRequest
from api.protocols import HttpRequest, HttpResponse


def error(message: str = 'Internal server error') -> Dict[str, str]:
    return {'error': message}

def bad_request(body: Dict[str, Any]) -> HttpResponse:
    return HttpResponse(status_code=400, body=body)

def created(body: Dict[str, Any]) -> HttpResponse:
    return HttpResponse(status_code=201, body=body)

def internal_server_error(body: Dict[str, Any]) -> HttpResponse:
    return HttpResponse(status_code=500, body=body)

def not_found(body: Dict[str, Any]) -> HttpResponse:
    return HttpResponse(status_code=404, body=body)

def success(body: Dict[str, Any]) -> HttpResponse:
    return HttpResponse(status_code=200, body=body)


def validate_required_params(request: HttpRequest, params: List[str]):
    for param in params:
        if(request.get(param) is None):
            raise BadRequest(f'Missing param {param}')


def parse_flask_request(request: FlaskRequest) -> HttpRequest:
    try: 
        body = request.json
        if(body is None): raise
        
        return HttpRequest(body=body) 
    
    except:
        return HttpRequest(body={})
