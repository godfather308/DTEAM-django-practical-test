from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DetailView, ListView

from services.email_service import is_email_valid
from services.pdf_service import get_pdf_filename, html_template_to_pdf
from .models import CV
from .tasks.email_tasks import send_cv_pdf


class CVListView(ListView):
    model = CV
    template_name = 'main/cv_list_view.html'
    context_object_name = 'cvs'

    def get_queryset(self):
        return CV.objects.prefetch_related('skills', 'projects', 'contacts').all()


class CVDetailView(DetailView):
    model = CV
    template_name = 'main/cv_detail_view.html'
    context_object_name = 'cv'

    def get_queryset(self):
        return CV.objects.prefetch_related('skills', 'projects', 'contacts')


def cv_download_pdf(request, pk):
    cv = get_object_or_404(CV.objects.prefetch_related('skills', 'projects', 'contacts'), pk=pk)
    pdf_file = html_template_to_pdf("main/cv_pdf_template.html", {"cv": cv})
    pdf_filename = get_pdf_filename(cv)
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{pdf_filename}"'
    return response


def cv_send_email(request, pk):
    if request.method != "POST":
        return HttpResponse("Invalid request method.", status=400)

    email = request.POST.get("email")
    if not email or not is_email_valid(email):
        return HttpResponse("Invalid email address.", status=400)

    send_cv_pdf.delay('main/cv_pdf_template.html', pk, email)

    return redirect('main:cv_detail_view', pk=pk)


def settings_view(request):
    return render(request, "main/settings.html")

