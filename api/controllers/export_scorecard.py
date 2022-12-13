from api.exceptions import BadRequest
from api.helpers import (
    bad_request, error, internal_server_error, success, validate_required_params
)
from api.models import StudentModel
from api.protocols import (
    Controller, HttpRequest, HttpResponse, PDFExporter, TemplateRender
)

def validate_students(request: HttpRequest):
    validate_required_params(request, ['students'])
        
    try:
        for item in list(request.body['students']):
            StudentModel.from_dict(item)
    except Exception as ex:
        raise BadRequest(ex)


class ExportScoreCardController(Controller):
    def __init__(self, template: TemplateRender, exporter: PDFExporter) -> None:
        self.template = template
        self.exporter = exporter    


    def make_pdf(self, request: HttpRequest) -> HttpResponse:
        html = self.template.render('scorecard/index.html', request.body)
        pdf  = self.exporter.export(html)

        response = success({'pdf': pdf})
        response.headers['Content-Type'] = 'application/pdf'
        #response.headers['Content-Disposition'] = 'attachment'
        response.headers['Content-Disposition'] = 'inline'
        return response


    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            validate_students(request)
            return self.make_pdf(request)

        except BadRequest as ex:
            return bad_request(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))
    
