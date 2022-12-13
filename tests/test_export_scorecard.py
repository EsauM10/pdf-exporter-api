from typing import Any, Dict
from pytest import MonkeyPatch

from api.controllers import ExportScoreCardController
from api.helpers import error
from api.protocols import HttpRequest, PDFExporter, TemplateRender


def missing_param_error(param: str) -> Dict[str, str]:
    return error(message=f'Missing param {param}')


def make_template_render() -> TemplateRender:
    class TemplateRenderMock(TemplateRender):
        def render(self, filename: str, data: Dict[str, Any]) -> str:
            return 'template'

    return TemplateRenderMock()


def make_pdf_exporter() -> PDFExporter:
    class PDFExporterMock(PDFExporter):
        def export(self, template: str) -> bytes:
            return b'template'
        
    return PDFExporterMock()


def make_controller() -> ExportScoreCardController:
    template = make_template_render()
    exporter = make_pdf_exporter()
    return ExportScoreCardController(template, exporter)


def test_should_return_400_if_students_is_not_provided():
    controller = make_controller()
    request  = HttpRequest(body={})
    response = controller.handle(request)
    assert response.status_code == 400
    assert response.body == missing_param_error('students')


def test_should_return_400_if_student_name_is_not_provided():
    controller = make_controller()
    request = HttpRequest(body={
        'students': [
            {'name': 'User1', 'score1': 1.0, 'score2': 2.0, 'score3': 3.0, 'mean': 2.0},
            {'score1': 1.0, 'score2': 2.0, 'score3': 3.0, 'mean': 2.0}
        ]
    })
    response = controller.handle(request)
    assert response.status_code == 400
    assert response.body == missing_param_error('name')


def test_should_return_400_if_student_score1_is_not_provided():
    controller = make_controller()
    request = HttpRequest(body={
        'students': [
            {'name': 'User1', 'score1': 1.0, 'score2': 2.0, 'score3': 3.0, 'mean': 2.0},
            {'name': 'User2', 'score2': 2.0, 'score3': 3.0, 'mean': 2.0}
        ]
    })
    response = controller.handle(request)
    assert response.status_code == 400
    assert response.body == missing_param_error('score1')


def test_should_return_400_if_student_score2_is_not_provided():
    controller = make_controller()
    request = HttpRequest(body={
        'students': [
            {'name': 'User1', 'score1': 1.0, 'score2': 2.0, 'score3': 3.0, 'mean': 2.0},
            {'name': 'User2', 'score1': 1.0, 'score3': 3.0, 'mean': 2.0}
        ]
    })
    response = controller.handle(request)
    assert response.status_code == 400
    assert response.body == missing_param_error('score2')


def test_should_return_400_if_student_score3_is_not_provided():
    controller = make_controller()
    request = HttpRequest(body={
        'students': [
            {'name': 'User1', 'score1': 1.0, 'score2': 2.0, 'score3': 3.0, 'mean': 2.0},
            {'name': 'User2', 'score1': 1.0, 'score2': 2.0, 'mean': 2.0}
        ]
    })
    response = controller.handle(request)
    assert response.status_code == 400
    assert response.body == missing_param_error('score3')


def test_should_return_400_if_student_mean_is_not_provided():
    controller = make_controller()
    request = HttpRequest(body={
        'students': [
            {'name': 'User1', 'score1': 1.0, 'score2': 2.0, 'score3': 3.0, 'mean': 2.0},
            {'name': 'User2', 'score1': 1.0, 'score2': 2.0, 'score3': 3.0}
        ]
    })
    response = controller.handle(request)
    assert response.status_code == 400
    assert response.body == missing_param_error('mean')


def test_should_return_400_if_incorrect_data_type_is_provided():
    controller = make_controller()
    request = HttpRequest(body={
        'students': [
            {'name': 'User1', 'score1': 1.0, 'score2': 2.0, 'score3': 3.0, 'mean': 2.0},
        ]
    })

    incorrect_data = {
        'score1': '1.0a', 
        'score2': 'abc', 
        'score3': 'any',
        'mean':   '(8.0)'
    }

    for key, value in incorrect_data.items():
        request.body['students'][0][key] = value
        response = controller.handle(request)
        assert response.status_code == 400


def test_should_return_500_if_template_render_raises(monkeypatch: MonkeyPatch):
    def render(filename, data):
        raise Exception('Server error')
    
    controller = make_controller()

    monkeypatch.setattr(controller.template, 'render', render)

    request = HttpRequest(body={
        'students': [
            {'name': 'User1', 'score1': 1.0, 'score2': 2.0, 'score3': 3.0, 'mean': 2.0},
        ]
    })
    response = controller.handle(request)
    assert response.status_code == 500
    assert response.body == error('Server error')



def test_should_return_500_if_pdf_exporter_raises(monkeypatch: MonkeyPatch):
    def export(template):
        raise Exception('Exporting error')
    
    controller = make_controller()
    monkeypatch.setattr(controller.exporter, 'export', export)

    request = HttpRequest(body={
        'students': [
            {'name': 'User1', 'score1': 1.0, 'score2': 2.0, 'score3': 3.0, 'mean': 2.0},
        ]
    })
    response = controller.handle(request)
    assert response.status_code == 500
    assert response.body == error('Exporting error')


def test_should_return_200_if_valid_data_is_provided():
    controller = make_controller()
    headers = {
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'inline'
    }

    request = HttpRequest(body={
        'students': [
            {'name': 'User1', 'score1': 1.0, 'score2': 2.0, 'score3': 3.0, 'mean': 2.0},
        ]
    })
    response = controller.handle(request)
    assert response.status_code == 200
    assert response.headers == headers
    assert response.body == {'pdf': b'template'}
