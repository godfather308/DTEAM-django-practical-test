from celery import shared_task
from django.core.mail import EmailMessage

from main.models import CV
from services.pdf_service import html_template_to_pdf, get_pdf_filename


@shared_task
def send_cv_pdf(template_path, cv_id, recipient_email):
    cv = CV.objects.get(pk=cv_id)
    pdf_file = html_template_to_pdf(template_path, {'cv': cv})

    email = EmailMessage(
        subject="CVProject sent your CV",
        body="Your CV is below this message",
        to=[recipient_email],
    )

    email.attach(get_pdf_filename(cv), pdf_file, "application/pdf")
    email.send()
