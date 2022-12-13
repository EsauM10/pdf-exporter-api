from api.protocols import PDFExporter
from weasyprint import HTML

class WeasyPrintExporter(PDFExporter):

    def export(self, html: str) -> bytes:
        pdf = HTML(string=html, base_url="").write_pdf()
        return b'' if(pdf is None) else pdf