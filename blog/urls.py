from django.conf.urls import url
from . import views


urlpatterns = [
    url(r"^akema/([0-9]+)/$", views.akema_temp, name="akema_temp"),
    url(r"^pdf/$", views.html_to_pdf_view, name="pdf",),
    url(r"", views.main_page, name="home_page"),
]
