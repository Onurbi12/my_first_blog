from django.conf.urls import url
from . import views


urlpatterns = [
    url(r"^akema\/$", views.new_html, name="akema_temp"),
    url(r"", views.main_page, name="home_page"),
]
