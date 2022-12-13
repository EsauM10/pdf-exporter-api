from typing import Any, Dict
from api.protocols import TemplateRender

from jinja2 import Environment, FileSystemLoader

enviroment = Environment(loader=FileSystemLoader('templates/'))

class JinjaTemplateRender(TemplateRender):
    def render(self, filename: str, data: Dict[str, Any]) -> str:
        template = enviroment.get_template(filename)
        return template.render(data)