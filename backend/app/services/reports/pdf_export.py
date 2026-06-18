# purpose: PDF Exporter | enforces: Quality-first
import json

class PDFExport:
    @staticmethod
    def export(report_data: dict) -> bytes:
        # Dummy PDF generation using JSON bytes
        header = b"%PDF-1.4\n"
        content = json.dumps(report_data, indent=2).encode('utf-8')
        return header + content + b"\n%%EOF"
