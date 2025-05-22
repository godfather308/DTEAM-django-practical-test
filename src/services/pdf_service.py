import weasyprint
from django.template.loader import get_template


def html_template_to_pdf(html_template_path, context):
    html_string = get_template(html_template_path).render(context)
    pdf_file = weasyprint.HTML(string=html_string).write_pdf()
    return pdf_file

def get_pdf_filename(cv):
    return f"CV_{cv.first_name}_{cv.last_name}.pdf"
