from django.conf.urls import url
from . import views
from wkhtmltopdf.views import PDFTemplateView


urlpatterns = [
    url(r"^akema/([0-9]+)/$", views.akema_temp, name="akema_temp"),
    url(
        r"^pdf/$",
        PDFTemplateView.as_view(
            template_name="blog/result.html", filename="my_pdf.pdf",
        ),
        name="pdf",
    ),
    url(r"", views.main_page, name="home_page"),
]
